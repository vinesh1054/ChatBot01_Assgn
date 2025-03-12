from langchain_community.chat_models import ChatOllama
llm = ChatOllama(model="llama3.1:8b")
response = llm.invoke("Hello!")
print(response)
