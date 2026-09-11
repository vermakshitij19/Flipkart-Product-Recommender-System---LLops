import os

from langchain_astradb import AstraDBVectorStore
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEndpointEmbeddings

from flipkart.data_converter import DataConverter
from flipkart.config import config


class DataIngestor:
    def __init__(self):
        self.embedding = HuggingFaceEndpointEmbeddings(model=config.EMBEDDING_MODEL)
        self.vstore = self._build_vector_store()

    def _build_vector_store(self):
        try:
            return AstraDBVectorStore(
                embedding=self.embedding,
                collection_name="flipkart_database",
                api_endpoint=config.ASTRA_DB_API_ENDPOINT,
                token=config.ASTRA_DB_APPLICATION_TOKEN,
                namespace=config.ASTRA_DB_KEY_SPACE,
            )
        except Exception:
            data_path = os.path.join("data", "flipkart_product_review.csv")
            if os.path.exists(data_path):
                docs = DataConverter(data_path).convert()
                vector_store = FAISS.from_documents(docs, self.embedding)
                vector_store.save_local("faiss_index")
                return vector_store

            return FAISS.from_texts(["No review data available."], self.embedding)

    def ingest(self, load_existing=True):
        if load_existing:
            if hasattr(self.vstore, "load"):
                try:
                    return self.vstore
                except Exception:
                    pass

            data_path = os.path.join("data", "flipkart_product_review.csv")
            if os.path.exists(data_path):
                try:
                    docs = DataConverter(data_path).convert()
                    return FAISS.from_documents(docs, self.embedding)
                except Exception:
                    return self.vstore

            return self.vstore

        docs = DataConverter(os.path.join("data", "flipkart_product_review.csv")).convert()

        if hasattr(self.vstore, "add_documents"):
            self.vstore.add_documents(docs)
            return self.vstore

        self.vstore = FAISS.from_documents(docs, self.embedding)
        self.vstore.save_local("faiss_index")
        return self.vstore