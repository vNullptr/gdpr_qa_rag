"""pydantic .env setup"""

from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):

    # API KEYS    
    OPENAI_API_KEY: str

    # LANGCHAIN
    LANGSMITH_TRACING: str
    LANGSMITH_ENDPOINT: str
    LANGSMITH_API_KEY: str
    LANGSMITH_PROJECT: str
    
    # CONFIG
    MODEL_NAME: str
    EMBEDDING_MODEL: str
    
    CHUNK_SIZE: int
    CHUNK_OVERLAP: int
    
    # CHROMA
    CHROMA_COLLECTION_NAME: str
    
    # RETRIEVAL
    TOP_K: int
    SEARCH_METHOD: str
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    def model_post_init(self, __context):
        if self.LANGSMITH_TRACING and self.LANGSMITH_API_KEY:
            os.environ["LANGSMITH_ENDPOINT"]= self.LANGSMITH_ENDPOINT
            os.environ["LANGSMITH_TRACING"] = self.LANGSMITH_TRACING
            os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY
            os.environ["LANGSMITH_PROJECT"] = self.LANGSMITH_PROJECT