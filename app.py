import streamlit as st
import os
import json
import numpy as np
import faiss
import openai
import time
from typing import List, Dict, Any

# Custom CSS for a beautiful UI
custom_css = """
<style>
/* Dynamic Heading */
.dynamic-heading {
    text-align: center;
    padding: 1.5rem;
    margin-bottom: 2rem;
    font-size: 2.5rem;
    font-weight: bold;
    color: #2c3e50;
    background: linear-gradient(135deg, #f5f7fa, #c3cfe2);
    border-radius: 0.75rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
}

/* Company Overlay */
.company-overlay {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-30deg);
    font-size: 10rem;
    font-weight: bold;
    opacity: 0.03;
    pointer-events: none;
    z-index: 1;
    color: #666;
    white-space: nowrap;
    user-select: none;
    width: 100%;
    text-align: center;
    font-family: 'Georgia', serif;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    text-align: center;
    padding: 0.75rem;
    background-color: #f8f9fa;
    border-top: 1px solid #e9ecef;
    z-index: 100;
    font-size: 0.9rem;
    color: #666;
    font-family: 'Arial', sans-serif;
}

/* Main container adjustments */
.main .block-container {
    z-index: 2;
    position: relative;
    padding-bottom: 6rem; /* Add padding for footer */
}

/* Chat messages container */
.stChatMessageContent {
    background-color: white;
    z-index: 2;
    position: relative;
    border-radius: 0.75rem;
    padding: 1rem;
    margin: 0.5rem 0;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* Notification */
.notification {
    text-align: center;
    font-size: 1.2rem;
    color: #4CAF50;
    margin-top: 1rem;
    padding: 0.75rem;
    background-color: #e8f5e9;
    border-radius: 0.5rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    animation: fadeOut 5s forwards;
}

@keyframes fadeOut {
    0% { opacity: 1; }
    100% { opacity: 0; }
}

/* Chat input box */
.stTextInput>div>div>input {
    border-radius: 0.75rem !important;
    padding: 0.75rem !important;
    font-size: 1rem !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Spinner styling */
.stSpinner>div {
    border-color: #4CAF50 !important;
}
</style>
"""

class ChatSystem:
    def __init__(self):
        self.index = faiss.IndexFlatL2(3072)  # Updated dimension to 3072
        self.metadata = []
        self.load_all_embeddings()
        
    def load_all_embeddings(self):
        """Load all embeddings from the embeddings directory"""
        embeddings_dir = "./embeddings"  # Directory containing all embedding files
        if not os.path.exists(embeddings_dir):
            st.error(f"Embeddings directory not found: {embeddings_dir}")
            return
        
        # Load all JSON files in the embeddings directory
        loaded_files = 0
        for filename in os.listdir(embeddings_dir):
            if filename.endswith(".json"):
                try:
                    file_path = os.path.join(embeddings_dir, filename)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    
                    for record in data:
                        embedding = np.array(record["embedding"]).astype('float32')
                        self.index.add(np.expand_dims(embedding, axis=0))
                        self.metadata.append({
                            "text": record["text"],
                            "source_file": record.get("source_file", filename),
                            "chunk_index": record.get("chunk_index", -1)
                        })
                    
                    loaded_files += 1
                except Exception as e:
                    st.error(f"Error loading embeddings from {filename}: {str(e)}")
        
        if loaded_files > 0:
            # Show a notification for 5 seconds
            st.markdown('<div class="notification">Ready to chat!</div>', unsafe_allow_html=True)
            time.sleep(5)  # Display the notification for 5 seconds
        else:
            st.error("No embeddings were loaded. Please check the embeddings directory.")

    def generate_embedding(self, text):
        """Generate embedding for query using text-embedding-3-large"""
        try:
            text = text.replace("\n", " ")
            response = openai.Embedding.create(
                input=text,
                model="text-embedding-3-large"  # Updated to use the large model
            )
            return response["data"][0]["embedding"]
        except Exception as e:
            st.error(f"Error generating embedding: {str(e)}")
            return None

    def get_answer_gpt4(self, question, context_chunks):
        """Generate answer using GPT-4"""
        try:
            context = "\n\n".join(context_chunks)
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # Use GPT-4
                messages=[
                    {"role": "system", "content": "You are a helpful Assistant that provides accurate information based on the provided knowledge base. Only use information from the given context. And important thing is don't use general Knowledge."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}\nAnswer:"}
                ],
                max_tokens=1800,
                temperature=0.7
            )
            return response["choices"][0]["message"]["content"].strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"

    def ask_question(self, question):
        """Query the system with a question"""
        try:
            question_embedding = self.generate_embedding(question)
            if question_embedding is None:
                return "Error processing question."
                
            question_embedding = np.expand_dims(np.array(question_embedding).astype('float32'), axis=0)
            distances, indices = self.index.search(question_embedding, 3)  # Get top 3 results
            relevant_chunks = [self.metadata[idx]["text"] for idx in indices[0]]
            return self.get_answer_gpt4(question, relevant_chunks)
            
        except Exception as e:
            return f"Error: {str(e)}"

def initialize_session_state():
    """Initialize session state variables"""
    if 'chat_system' not in st.session_state:
        st.session_state.chat_system = ChatSystem()
    if 'messages' not in st.session_state:
        st.session_state.messages = []

def main():
    # Configure the page
    st.set_page_config(
        page_title="Mahaperiyava",
        page_icon="📚",
        layout="wide"
    )

    # Initialize session state
    initialize_session_state()

    # Apply custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Add company overlay
    st.markdown('<div class="company-overlay">Mahaperiyava</div>', unsafe_allow_html=True)

    # Add footer
    st.markdown(
        '<div class="footer">Developed by CAp corporate AI solutions LLP</div>',
        unsafe_allow_html=True
    )

    # Add page heading
    st.markdown(
        '<div class="dynamic-heading">Mahaperiyava AI GPT</div>',
        unsafe_allow_html=True
    )

    # Initialize OpenAI key
    openai.api_key = "apikey"  # Replace with your actual API key
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Type your question here..."):
        # Add user message
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        # Display user message immediately
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Display a loading spinner while generating the response
        with st.spinner("Generating response..."):
            response = st.session_state.chat_system.ask_question(prompt)
        
        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
        
        # Display assistant message
        with st.chat_message("assistant"):
            st.markdown(response)

if __name__ == "__main__":
    main()