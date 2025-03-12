import streamlit as st
import json
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from config import OLLAMA_MODEL

# File to store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# Load previous chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file:
            return json.load(file)
    return []

# Save chat history
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Initialize memory with past chat history
past_chats = load_chat_history()
memory = ConversationBufferMemory(memory_key="history")
for chat in past_chats:
    memory.chat_memory.add_user_message(chat["user"])
    memory.chat_memory.add_ai_message(chat["bot"])

# Define custom chat prompt template
chat_prompt = PromptTemplate(
    input_variables=["history", "input"],
    template="""
    You are Vinesh, a helpful AI assistant.
    - If the user greets you (e.g., 'hello', 'hi', 'hey'), respond with a friendly greeting.
    - If the user asks 'Who are you?' or 'Who you are?', always reply with: 'I am Vinesh'.
    - Otherwise, answer the question naturally.

    Previous conversation:
    {history}

    User: {input}
    AI:"""
)

# Set up LLaMA 3 model with the custom prompt
chat_model = ChatOllama(model=OLLAMA_MODEL)
chat = ConversationChain(llm=chat_model, memory=memory, prompt=chat_prompt)

# Streamlit UI
st.set_page_config(page_title="LLaMA 3.1-8B Chatbot", layout="wide")
st.title("🦙 LLaMA 3.1-8B Chatbot")

st.write("A chatbot powered by LLaMA 3.1-8B.")

# Chat history UI
if "messages" not in st.session_state:
    st.session_state.messages = past_chats

# Display chat history
for message in st.session_state.messages:
    st.write(f"**You:** {message['user']}")
    st.write(f"**Bot:** {message['bot']}")

# User input (Press Enter to send)
user_input = st.text_input("You:", key="user_input", placeholder="Type your message here and press Enter...")

if user_input:  # When user presses Enter, this triggers
    # Get chatbot response
    response = chat.run({"input": user_input})

    # Store in chat history
    st.session_state.messages.append({"user": user_input, "bot": response})
    save_chat_history(st.session_state.messages)

    # Display new conversation
    st.write(f"**You:** {user_input}")
    st.write(f"**Bot:** {response}")

    # Clear input field manually (if needed, but not required)
    # st.session_state["user_input"] = ""
