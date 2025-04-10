import os
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
from pymongo import MongoClient

load_dotenv()

class ChatBot:
    def __init__(self, api_key, model="mistral"):
        self.api_key = api_key
        self.model = model
        self.conversation_history = []
        self.mistral_client = ChatMistralAI(api_key=api_key)
        self.qa_chain = self.initialize_context()


    def initialize_context(self):
        # Fetch MongoDB connection info from environment
        mongo_uri = os.getenv("MONGO_URI")
        db_name = os.getenv("MONGO_DB_NAME")
        collection_name = os.getenv("MONGO_COLLECTION_NAME")

        # Connect to MongoDB
        client = MongoClient(mongo_uri)
        db = client[db_name]
        collection = db[collection_name]

        # Fetch and embed documents
        profiles = list(collection.find({}, {"_id": 0}))
        docs = [Document(page_content="\n".join(f"{k}: {v}" for k, v in p.items())) for p in profiles]

        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        retriever = vectorstore.as_retriever(search_type="similarity", k=3)

        return RetrievalQA.from_chain_type(
            llm=self.mistral_client,
            retriever=retriever,
            return_source_documents=False
        )

    def get_user_input(self):
        user_input = input("\nYou: ")
        return user_input

    def send_request(self, query):
        response = self.qa_chain.invoke(query)['result']
        return response

    def chat_loop(self):
        print("🧠 Profile ChatBot Ready (type 'exit' to quit)")
        while True:
            query = self.get_user_input()
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
            response = self.send_request(query)
            print(f"Bot: {response}")


if __name__ == "__main__":
    api_key = os.getenv("MISTRAL_API_KEY")
    bot = ChatBot(api_key=api_key)
    bot.chat_loop()
