from langchain_chroma import Chroma
from rag.config import Settings
from rag.shared.embedding import EmbeddingProvider
from uuid import uuid4

class VectorDatabase:
    """
    Creates a ChromaDB Connection/Instance
    """
    def __init__(self):
        settings = Settings()
        embedding_provider = EmbeddingProvider()
        
        self.__instance = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=embedding_provider.embedding_function,
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
        
    def get_retriever(self, method: str, top_k: int):
        """Derives a retriever from the vector store with specified search method and top_k.

        Args:
            method (str): The search method.
            top_k (int): The amount of neighbours to retrieve.

        Returns:
            Returns a runnable retriever object.
        """
        return self.__instance.as_retriever(
            search_type=method,
            search_kwargs={
                "k":top_k
            }
        )