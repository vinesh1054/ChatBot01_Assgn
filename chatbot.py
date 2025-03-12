import json
import os
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from config import OLLAMA_MODEL

# File where I will store chat history
CHAT_HISTORY_FILE = "chat_history.json"

# load_chat_history() will load previous chat history
def load_chat_history():
    if os.path.exists(CHAT_HISTORY_FILE):
        with open(CHAT_HISTORY_FILE, "r") as file: # in read mode
            return json.load(file)
    return []

# Saving chat history
def save_chat_history(history):
    with open(CHAT_HISTORY_FILE, "w") as file: #in write mode
        json.dump(history, file, indent=4)

# Initialize memory with past chat history
past_chats = load_chat_history()
memory = ConversationBufferMemory() #To remember context across multiple user inputs.
for chat in past_chats:
    memory.chat_memory.add_user_message(chat["user"]) #Stores the user’s message
    memory.chat_memory.add_ai_message(chat["bot"])    #Stores the chatbot’s message

# Define custom chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Vinesh, a helpful AI assistant. You should respond to greetings appropriately. "
               "If the user asks 'Who are you?' or 'Who you are?', always reply with 'I am Vinesh'."),
    ("user", "{input}")
])

# Set up LLaMA 3 model with the custom prompt
chat_model = ChatOllama(model=OLLAMA_MODEL)
chat = ConversationChain(llm=chat_model, memory=memory, prompt=chat_prompt)

def chat_with_model():
    print("Chatbot is ready! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        
        response = chat.run(user_input)
        
        # Save chat history
        past_chats.append({"user": user_input, "bot": response})
        save_chat_history(past_chats)
        
        print(f"Bot: {response}")

if __name__ == "__main__":
    chat_with_model()
