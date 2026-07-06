from langchain_openai import OpenAIEmbeddings
from rag.config import Settings
import openai

import logging 
logger = logging.getLogger(__name__)

class EmbeddingProviderError(Exception): pass

class EmbeddingProvider:
    """
    Validates api key and initializes the OpenAI embedding function.
    """
    def __init__(self):
        settings = Settings()
        self.__client = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY, model=settings.EMBEDDING_MODEL)
        
        # NOTE: i don't know if this is actually worth keeping, i think its a good idea to check if the api key is valid before doing anything else.
        try:
            self.__client.embed_query("ping")
        except openai.AuthenticationError as e:
            logger.exception("Embedding provider failed to authenticate.")
            raise EmbeddingProviderError("Embedding provider failed to authenticate.")
  
    @property
    def embedding_function(self):
        """
        Returns:
            Returns the embedding function. 
        """
        return self.__client