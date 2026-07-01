"""pydantic .env setup"""


from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    # LLM    
    OPENAI_API_KEY: str

    # LANGCHAIN
    
    
    
    model_config = SettingsConfigDict(env_file=".env", env_prefix="config_")