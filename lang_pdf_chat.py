from langchain_community.embeddings.ollama import OllamaEmbeddings
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain_community.document_loaders import AzureAIDocumentIntelligenceLoader
from dotenv import load_dotenv
import os

load_dotenv()

azuredoc_endpoint = os.environ["azuredoc_endpoint"]
azuredoc_apikey = os.environ["azuredoc_apikey"]
file_path = "./doc/上誼3.docx"
loader1 = AzureAIDocumentIntelligenceLoader(
    api_endpoint=azuredoc_endpoint, api_key=azuredoc_apikey, file_path=file_path, api_model="prebuilt-layout"
)
documents = loader1.load()

# 讀取檔案
#file_path = "./ResumeSomer.pdf"
#loader = file_path.endswith(".pdf") and PyPDFLoader(file_path) or TextLoader(file_path)

# 選擇 splitter 並將文字切分成多個 chunk 
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0) 
texts = loader1.load_and_split(splitter)

# 建立本地 db
embeddings = OllamaEmbeddings(model= "llama3.1:latest")
vectorstore = Chroma.from_documents(texts, embeddings)

# 對話 chain
qa = ConversationalRetrievalChain.from_llm(ChatOllama(model="llama3.1:latest", temperature=0), vectorstore.as_retriever())
chat_history = []
while True:
    query = input('\nQ: ') 
    if not query:
        break
    result = qa({"question": query + '不要有幻覺，不確定的資訊請直接說不知道(用繁體中文回答)', "chat_history": chat_history})
    print('A:', result['answer'])
    chat_history.append((query, result['answer']))

# query = "What is the publisher of this book? Only answer the name."

# result = qa({"question": query + '直接回答該檔案的出版社名稱', "chat_history": chat_history})
# print(result['answer'])