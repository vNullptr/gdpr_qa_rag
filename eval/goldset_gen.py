import httpx
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.documents import Document
from ragas.testset import TestsetGenerator
from ragas.testset.synthesizers import single_hop, multi_hop

from rag.config import Settings
from rag.ingestion.parser import GDPRHTMLParser


class GoldSetGenerator:
    def __init__(self, path):
        settings = Settings()
        
        with open(path,"r") as f:    
            parsed_docs = GDPRHTMLParser(f.read()).parse()
            self.docs = [Document(**article) for article in parsed_docs.articles]
        
        no_keepalive_limits = httpx.Limits(max_keepalive_connections=0)
        generator_llm = ChatOpenAI(
            model=settings.MODEL_NAME,
            api_key=settings.OPENAI_API_KEY,
            http_async_client=httpx.AsyncClient(limits=no_keepalive_limits),
        )
        generator_embedding = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            api_key=settings.OPENAI_API_KEY,
            http_async_client=httpx.AsyncClient(limits=no_keepalive_limits),
        )
        self.generator = TestsetGenerator.from_langchain(
            generator_llm,
            generator_embedding,
            
            )
        
    def generate(self, size=10):
        dataset = self.generator.generate_with_langchain_docs(self.docs, testset_size=size)
        print(dataset.to_pandas())
        return dataset
    
    
if __name__ == "__main__":
    gset_gen = GoldSetGenerator("./documents/eu_gdpr.html")
    gset_gen.generate(29)
        
        