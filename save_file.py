from pymongo import MongoClient
from docx import Document
from dotenv import load_dotenv
import os
import base64

load_dotenv()

os.environ["MONGO_URI"] = os.getenv("MONGO_URI")
mongo_uri = os.getenv("MONGO_URI")


def read_docx_as_base64(file_path):
    with open(file_path, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode('utf-8')
    return encoded_string

# 連接到 MongoDB 並儲存文件內容的函數
def store_to_mongodb(file_content_base64, collection_name, db_name='test'):
    # 連接到 MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # 建立要插入的文件
    document = {
        "file_content_base64": file_content_base64
    }

    # 插入文件到集合中
    result = collection.insert_one(document)
    print(f"文件已插入，ID 為: {result.inserted_id}")

# 主函數
def main():
    file_path = './doc/上誼.docx'  # 將這裡替換為你的 .docx 檔案路徑
    collection_name = 'doc'  # 將這裡替換為你想要的集合名稱

    # 讀取 .docx 檔案並編碼為 Base64
    file_content_base64 = read_docx_as_base64(file_path)

    # 將內容儲存到 MongoDB
    store_to_mongodb(file_content_base64, collection_name)

if __name__ == '__main__':
    main()

