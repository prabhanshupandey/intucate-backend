from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["intucate_db"]

prompts_collection = db["prompts"]
history_collection = db["history"]