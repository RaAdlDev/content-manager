from pydantic_settings import SettingsConfigDict, BaseSettings

class Settings(BaseSettings):
    database_url:str
    secret_key: str
    algorithm: str
    token_duration: int
    testing_database_url: str
    debug: bool = False

    model_config = SettingsConfigDict(env_file=".env")
    
settings = Settings()