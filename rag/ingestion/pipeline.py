from langsmith import traceable 

from rag.ingestion.parser import GDPRHTMLParser

class IngestionPipeline:
    """
    Defines the Ingestion pipeline from embedding documents and storing in the vector database.
    """
    def __init__(self, document_path):
    
        with open(document_path, "r", encoding="utf-8") as file: 
            self.loaded_doc = file.read()

        
        
    
    @traceable(name="Pipeline Ingestion")
    def ingest(self):
        """Ingests documents and stores them in vector database."""
        parser = GDPRHTMLParser(self.loaded_doc)
        parser.parse()
        print(parser.articles)
        
        return "Documents will be ingested !"
        
        
    
        