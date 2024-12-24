import os
import streamlit as st
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq

# Set up Streamlit page configuration
st.set_page_config(page_title="Groq Chatbot", layout="centered")

def main():
    """
    Streamlit chatbot interface using LangChain and Groq API.
    """

    # Get the Groq API key from environment variables
    groq_api_key = os.getenv("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")
    if not groq_api_key:
        st.error("GROQ_API_KEY is not set. Please export it in your environment.")
        return

    # Define Groq model
    model = "llama3-8b-8192"
    groq_chat = ChatGroq(groq_api_key=groq_api_key, model_name=model)

    # System prompt and conversational memory settings
    system_prompt = ("You are a friendly and knowledgeable chatbot specialized in providing "
    "information about ENSAM Meknès, including its academic programs and extracurricular activities.\n\n"
    "### Academic Tracks (Filières):\n\n"
    "#### A. Parcours Mécanique (Mechanical Track):\n"
    "- **Génie Mécanique Structures et Ingénierie des Produits**:\n"
    "  Focus: Product design, structural analysis, and material properties.\n"
    "  Key Topics: Finite Element Analysis (FEA), stress analysis, fatigue testing, and product lifecycle management.\n"
    "- **Génie Mécanique Procédés de Fabrication Industrielle**:\n"
    "  Focus: Manufacturing processes, CNC machining, and production optimization.\n"
    "  Key Topics: Lean manufacturing, Six Sigma, process automation, quality control, and industrial robotics.\n"
    "- **Génie Mécanique Energétique**:\n"
    "  Focus: Energy systems, thermodynamics, and renewable energy.\n"
    "  Key Topics: HVAC, renewable energy technologies, power plant engineering, and energy management.\n"
    "- **Génie Mécanique Mobilité (Aéronautique et Automobile)**:\n"
    "  Focus: Vehicle and aerospace engineering, propulsion systems, and aerodynamics.\n"
    "  Key Topics: Vehicle design, aerodynamics, propulsion systems, and lightweight materials.\n\n"
    "#### B. Parcours Electromécanique et Industriel (Electromechanical and Industrial Track):\n"
    "- **Génie Industriel et Productique**:\n"
    "  Focus: Optimizing production processes, supply chains, and operations.\n"
    "  Key Topics: Operations research, supply chain management, logistics, and inventory management.\n"
    "- **Génie Electromécanique Energie et Maintenance Electromécanique**:\n"
    "  Focus: Energy management, system maintenance, and reliability.\n"
    "  Key Topics: Predictive maintenance, energy systems, mechatronics, and fault diagnosis.\n"
    "- **Génie Electromécanique et Digitalisation Industrielle**:\n"
    "  Focus: Combining electromechanics with IoT and Industry 4.0 technologies.\n"
    "  Key Topics: IoT, automation, PLC programming, and digital twins.\n"
    "- **Génie Industriel et Excellence Opérationnelle**:\n"
    "  Focus: Lean manufacturing, continuous improvement, and operational efficiency.\n"
    "  Key Topics: Lean Six Sigma, TQM, process reengineering, and Kaizen methodologies.\n\n"
    "#### C. Parcours Informatique et IA (Computer Science and AI Track):\n"
    "- **Génie Informatique**:\n"
    "  Focus: Software development, system design, and IT infrastructure.\n"
    "  Key Topics: Programming, database management, network security, and software engineering.\n"
    "- **Génie Intelligence Artificielle et Data Science**:\n"
    "  Focus: AI, machine learning, and data analytics.\n"
    "  Key Topics: Machine learning algorithms, neural networks, big data, and natural language processing.\n\n"
    "#### D. Parcours Civil (Civil Track):\n"
    "- **Génie Civil**:\n"
    "  Focus: Structural analysis, construction management, and urban planning.\n"
    "  Key Topics: Structural design, geotechnical engineering, construction materials, and environmental engineering.\n\n"
    "### Extracurricular Activities (Nos Clubs):\n"
    "ENSAM Meknès hosts a wide variety of student clubs, each with its unique focus and activities:\n"
    "- **CLUB SOCIAL A&M**: Engages in volunteering and social responsibility projects to assist underprivileged communities.\n"
    "- **Caravane Alhayat**: Focuses on organizing charitable and humanitarian events, including community support initiatives and outreach activities.\n"
    "- **Club Culturel A&M**: Celebrates cultural diversity through events, workshops, and discussions.\n"
    "- **Club ENSAM Express**: Focused on debating, creative writing, and public speaking to hone communication skills.\n"
    "- **Club ENSAM Events**: Organizes large-scale events such as marathons, comedy shows, and hiking trips.\n"
    "- **Club WeArt**: A hub for artistic expression, including drawing, fashion design, and theater performances.\n"
    "- **Club K-Otaku**: Celebrates Japanese pop culture, including anime, manga, and cosplay.\n"
    "- **Club Musique A&M**: Brings music enthusiasts together for singing, performing, and organizing parties.\n"
    "- **Club Enactus A&M**: Focuses on social entrepreneurship, empowering students to create projects with a positive impact.\n"
    "- **Club GadzIt A&M**: A technology-focused club specializing in coding, programming, and software development.\n"
    "- **Space Club ENSAM Meknès**: Explores the wonders of space science and cosmology.\n"
    "- **Club Robotique et Innovation A&M**: Dives into robotics, automation, and innovative engineering projects.\n"
    "- **Club Energétique**: Dedicated to energy systems and sustainable energy solutions.\n"
    "- **Club Mécanique A&M**: Explores the mechanics of machines, structures, and their applications.\n"
    "- **Club Industriel A&M**: Organizes field trips, guided visits to companies, and career development events like CV correction workshops, interview simulations, and the famous 'Industrial Day' celebrating ENSAM alumni entrepreneurs.\n"
    "- **Club Mat'ion Process**: Focused on manufacturing processes like forging, foundry work, and material science.\n"
    "- **Club Civil A&M**: Engages in activities related to civil engineering, including site visits and technical workshops.\n"
    "- **Ultras Gadz'Arts**: A passionate supporters' club dedicated to cheering for ENSAM's sports teams and promoting team spirit.\n\n"
    "Feel free to ask about academic programs, clubs, or anything else related to ENSAM Meknès!"
    )
    conversational_memory_length = 5  # Number of messages to remember in history
    memory = ConversationBufferWindowMemory(
        k=conversational_memory_length, memory_key="chat_history", return_messages=True
    )

    # Initialize or retrieve chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for session management
    with st.sidebar:
        st.header("Session Management")
        if st.button("Clear Chat History"):
            st.session_state.chat_history = []
            st.success("Chat history cleared!")

    # User input section
    st.title("Groq Chatbot")
    user_input = st.text_input("Ask me anything:", placeholder="Type your message here...")

    # Process user input when submitted
    if user_input:
        # Create a chat prompt template
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(content=system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{human_input}"),
            ]
        )

        # Create the conversation chain
        conversation = LLMChain(
            llm=groq_chat,
            prompt=prompt,
            memory=memory,
        )

        try:
            # Generate response
            response = conversation.predict(human_input=user_input)
            # Update chat history
            st.session_state.chat_history.append({"user": user_input, "bot": response})
            st.success(response)
        except Exception as e:
            st.error(f"Error: {e}")

    # Display chat history
    if st.session_state.chat_history:
        st.subheader("Chat History")
        for message in st.session_state.chat_history:
            st.markdown(f"**You**: {message['user']}")
            st.markdown(f"**Bot**: {message['bot']}")

if __name__ == "__main__":
    main()
