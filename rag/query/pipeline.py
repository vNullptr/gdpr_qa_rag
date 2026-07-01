

class QueryPipeline:
    """
    Defines the Query pipeline from embedding the query to retrieving top-k values/documents and citations to answer.
    """
    def __init__(self):
        pass
    
    def answer(self, qst)-> dict:
        """Answers a question based on documents
        
        Returns:
            A tuple (string answer, citations) representing what the llm answered based on retrieved documents.
        """
        citations: list[str] = []
        answer: str = ""
        
        return {"answer":answer, "citations":citations}