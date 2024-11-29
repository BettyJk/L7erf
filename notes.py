import streamlit as st
from transformers import AutoModelForCausalLM, AutoTokenizer
from sentence_transformers import SentenceTransformer
import faiss
import json
import torch
import requests
from bs4 import BeautifulSoup
import os

# Paths
model_name = r"C:\Users\admin\l7erf-bot\model"
data_folder = r"C:\Users\admin\l7erf-bot\data"

# Load models
st.spinner("Chargement des modèles...")
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
embedding_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2")

# Create FAISS index
@st.cache_resource
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

# Initialize FAISS
faiss_index, docs = create_faiss_index()

# Search FAISS index
def search_faiss_index(query):
    query_embedding = embedding_model.encode(query).reshape(1, -1)
    _, indices = faiss_index.search(query_embedding, 1)
    best_match = indices[0][0]
    return docs[best_match][1]

# Fallback: Fetch data from the web
def fetch_web_data(query):
    search_url = f"https://www.google.com/search?q={query}&hl=fr"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    result = soup.find("div", {"class": "BNeawe"})
    return result.text if result else "Aucune information trouvée."

# Fine-tuned GPT Model Response
def generate_gpt_response(query):
    prompt = f"Question: {query}\nRéponse:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(
        inputs.input_ids,
        max_length=200,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )
    return tokenizer.decode(outputs[0], skip_special_tokens=True).split("Réponse:")[-1].strip()

# Streamlit App
st.title("Chatbot IA en Français")
query = st.text_input("Posez votre question ici:")

if query:
    with st.spinner("Recherche en cours..."):
        # Step 1: Check FAISS
        faiss_response = search_faiss_index(query)

        # Step 2: GPT model fallback
        if not faiss_response:
            st.write("Aucun résultat trouvé dans les données locales. Recherche avec le modèle GPT...")
            gpt_response = generate_gpt_response(query)
            response = gpt_response
        else:
            response = faiss_response

        # Step 3: Web fallback
        if not response:
            st.write("Recherche en ligne...")
            response = fetch_web_data(query)

    st.write("### Réponse :", response)
