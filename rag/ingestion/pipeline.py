from langsmith import traceable 

class IngestionPipeline:
    """
    Defines the Ingestion pipeline from embedding documents and storing in the vector database.
    """
    def __init__(self):
        pass
    
    @traceable(name="Pipeline Ingestion")
    def ingest(self):
        """Ingests documents and stores them in vector database."""
        return "Documents will be ingested !"
        
        
    
        