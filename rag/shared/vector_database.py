from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from rag.config import Settings
from uuid import uuid4

class VectorDatabase:
    """
    Creates a ChromaDB Connection/Instance
    """
    def __init__(self):
        self.settings = Settings()
        self.__instance = Chroma(
            collection_name=self.settings.CHROMA_COLLECTION_NAME,
            embedding_function=OpenAIEmbeddings(model=self.settings.EMBEDDING_MODEL, api_key=self.settings.OPENAI_API_KEY),
            persist_directory="./vector_database"
        )
            
        
    def add(self, chunks: list[dict]):
        """Generates Unique IDs for a list of documents and adds them to the VectorStore

        Args:
            chunks (list): list of documents 

        Returns:
            VectorDatabase instance
        """
        
        uuids = [str(uuid4()) for _ in range(len(chunks))]
        self.__instance.add_documents(chunks, ids=uuids)
        
        return self
        
    def reset(self):
        """
        Resets the collection by deleting and recreating it.
        """
        self.__instance.reset_collection()
        