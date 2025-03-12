import json
import os
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_models import ChatOllama
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

# # Initialize memory with past chat history
# past_chats = load_chat_history()
# memory = ConversationBufferMemory() #To remember context across multiple user inputs.
# for chat in past_chats:
#     memory.chat_memory.add_user_message(chat["user"]) #Stores the user’s message
#     memory.chat_memory.add_ai_message(chat["bot"])    #Stores the chatbot’s message
# Initialize memory with past chat history
past_chats = load_chat_history()
memory = ConversationBufferMemory()  # To remember context across multiple user inputs.

for chat in past_chats:
    user_message = chat.get("user", "")
    bot_message = chat.get("bot", "")

    if isinstance(user_message, str):  # Ensure it's a string
        memory.chat_memory.add_user_message(user_message)
    
    if isinstance(bot_message, str):  # Ensure it's a string
        memory.chat_memory.add_ai_message(bot_message)


# Define custom chat prompt template
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are Vinesh, a helpful AI assistant. You should respond to greetings (such as 'Hi', 'Hey', 'Hello') with an appropriate greeting. "
               "If the user asks 'Who are you?' or 'Who you are?', always reply with 'I am Vinesh'. "
               "For all other inputs, respond normally."),
    ("user", "{history}\nUser: {input}")
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
        
        # response = chat.run(user_input)
        response = chat.invoke({"input": user_input})

        
        # Save chat history
        past_chats.append({"user": user_input, "bot": response})
        save_chat_history(past_chats)
        
        # print(f"Bot: {response}")
        if isinstance(response, dict) and "response" in response:
            formatted_response = response["response"]
        else:
            formatted_response = response  # Handle plain string responses

        print(f"Bot: {formatted_response}")

        

if __name__ == "__main__":
    chat_with_model()
