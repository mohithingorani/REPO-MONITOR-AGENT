from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name:str = "AGENT_API"
    debug:bool = False
    environment = "dev"

    class Config:
        env_file = ".env"

settings = Settings()