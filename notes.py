from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import json
import streamlit as st
import requests
from bs4 import BeautifulSoup
import torch
import os 
model_name = r"C:\Users\admin\l7erf-bot\fine_tune_gpt_j"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

embedding_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

data_folder = r"C:\Users\admin\l7erf-bot\data"

def create_faiss_index():
    embeddings = []
    docs = []
    for filename in os.listdir(data_folder):
        if filename.endswith(".json"):
            with open(os.path.join(data_folder, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for entry in data:
                    question = entry["question"]
                    response = entry["response"]
                    embedding = embedding_model.encode(question)
                    embeddings.append(embedding)
                    docs.append((question, response))
    
    embeddings = torch.tensor(embeddings).numpy()
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, docs

faiss_index, docs = create_faiss_index()

def search_faiss_index(query):
    query_embedding = embedding_model.encode(query).reshape(1, -1)
    _, indices = faiss_index.search(query_embedding, 1)
    best_match = indices[0][0]
    return docs[best_match][1]

def fetch_web_data(query):
    search_url = f"https://www.google.com/search?q={query}&hl=fr"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("div", {"class": "BNeawe"})
    return result.text if result else "Aucune information trouvée."

st.title("Chatbot IA en Français")
query = st.text_input("Posez votre question ici:")

if query:
    st.spinner("Recherche en cours...")
    faiss_response = search_faiss_index(query)
    response = faiss_response if faiss_response else fetch_web_data(query)
    st.write("Réponse:", response)
