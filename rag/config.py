"""pydantic .env setup"""


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # API KEYS    
    OPENAI_API_KEY: str

    # LANGCHAIN
    
    # CONFIG
    MODEL_NAME: str
    
    
    model_config = SettingsConfigDict(env_file=".env")