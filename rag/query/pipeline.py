from langsmith import traceable 
from langchain_core.runnables import RunnablePassthrough
from rag.shared.vector_database import VectorDatabase

class QueryPipeline:
    """
    Defines the Query pipeline from embedding the query to retrieving top-k values/documents and citations to answer.
    """
    def __init__(self):
        pass
    
    @traceable(name="Pipeline Answer")
    def query(self, query)-> dict:
        """Answers a question based on documents
        
        Returns:
            A tuple (string answer, citations) representing what the llm answered based on retrieved documents.
        """
        citations: list[str] = []
        answer: str = ""
        
        vector_db = VectorDatabase()
        retriever = vector_db.get_retriever(method="similarity", top_k=2)
        
        
        return {"answer":answer, "citations":citations}
    
    
    
if __name__ == "__main__":
    query_ppl = QueryPipeline()
   
    query_ppl.query("What is the right to erasure?") 