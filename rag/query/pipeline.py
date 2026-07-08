from langsmith import traceable
from langsmith.wrappers import wrap_openai
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from rag.shared.vector_database import VectorDatabase
from langchain_openai import ChatOpenAI
from rag.query import prompts
from rag.config import Settings


class QueryPipeline:
    """
    Defines the Query pipeline from embedding the query to retrieving top-k values/documents and citations to answer.
    """
    def __init__(self):
        self.settings = Settings()
        self.llm = ChatOpenAI(model=self.settings.MODEL_NAME, api_key=self.settings.OPENAI_API_KEY)
    
    @traceable(name="Pipeline Answer")
    def query(self, query: str)-> dict:
        """Answers a question based on documents
        
        Returns:
            A tuple (string answer, citations) representing what the llm answered based on retrieved documents.
        """
        
        vector_db = VectorDatabase()
        retriever = vector_db.get_retriever(method=self.settings.SEARCH_METHOD, top_k=self.settings.TOP_K)
        
        # I need to keep the retrieved documents so i can use them for references
        chain = ({"documents":retriever, "question": RunnablePassthrough()}
        | RunnablePassthrough.assign(
            answer=(prompts.BASE_PROMPT 
                    | self.llm 
                    | StrOutputParser()
                    )
        ))
        
        result = chain.invoke(query)
        references = [doc.metadata for doc in result["documents"]]
        
        return {"answer":result["answer"], "citations":references}
    