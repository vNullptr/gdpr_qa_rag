from langsmith import traceable
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rag.config import Settings
from rag.ingestion.parser import GDPRHTMLParser
from rag.shared.vector_database import VectorDatabase


class IngestionPipeline:
    """
    Defines the Ingestion pipeline from embedding documents and storing in the vector database.
    """
    def __init__(self, document_path: str):
    
        # Need to check if path exists before trying to open.
        with open(document_path, "r", encoding="utf-8") as file: 
            self.loaded_doc = file.read()
            self.settings = Settings()


    @traceable(run_type="embedding", name="Ingestion Pipeline")
    def ingest(self):
        """Ingests documents and stores them in vector database."""
        
        parser = GDPRHTMLParser(self.loaded_doc)
        parser.parse()
        
        chunks = self.chunk(parser.articles)
        
        documents = [Document(page_content=chunk["text"], metadata=chunk["metadata"]) for chunk in chunks]
        
        vector_db = VectorDatabase()
        vector_db.reset()
        vector_db.add(documents)
        
        return documents
    
    def chunk(self, articles: list[dict]):
        """chunks a list of articles.

        Args:
            articles (list[dict]): the list of articles to chunk.

        Returns:
            Returns a list of dictionnaries of the chunked articles 
        """
        # TODO: tune the chunking, i get some 3 characters chunks.     
        # Either clean them up before chunking or ignoring them.
        splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            model_name=self.settings.EMBEDDING_MODEL,
            chunk_size=self.settings.CHUNK_SIZE,
            chunk_overlap=self.settings.CHUNK_OVERLAP,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        
        chunks = []
        for article in articles:
            chunk = {"metadata":article["metadata"]}
            for text_chunk in splitter.split_text(article["text"]):
                chunk["text"] = text_chunk
                chunks.append(chunk.copy())
        
        return chunks
            
    
if __name__ == "__main__":
    ppl = IngestionPipeline("./documents/eu_gdpr.html")
    ppl.ingest()
