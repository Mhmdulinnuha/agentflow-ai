from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AgentFlow AI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    DB_HOST: str = "127.0.0.1"
    DB_PORT: int = 3306
    DB_NAME: str = "agentflow_ai"
    DB_USER: str = "root"
    DB_PASSWORD: str = "nuha220705"
    
    JWT_SECRET_KEY: str = "your-secret-key"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()