from pymongo import MongoClient
import pymongo
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv["OPENAI_API_KEY"]
os.environ["MONGO_URI"] = os.getenv("MONGO_URI")


llm = ChatOpenAI(temperature=0)
prompt_template = PromptTemplate(
    input_variables=["question", "context"],
    template="請你根據用戶輸入隨機生成10個字的內容。"
)
llm_chain = LLMChain(
    llm=llm,
    prompt=prompt_template
)
question =  "新書"
llm_rule = llm_chain.run(question=question)

# 連接 MongoDB 資料庫
mongo_uri = os.env["MONGO_URI"]
client = pymongo.MongoClient(mongo_uri)
db = client["test"]
collection = db["rules"]

supplier_name = "test_supplier222"
rule = llm_rule

document = {
    "supplier_name": supplier_name,
    "rules": rule
}

result = collection.insert_one(document)
print("Inserted document with _id =", result.inserted_id)
