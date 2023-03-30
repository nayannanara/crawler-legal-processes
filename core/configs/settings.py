from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Configuraçoes gerais usadas na aplicação
    """

    API_VERSION: str = '/api/v0'
    DB_URL: str = 'postgresql+asyncpg://crawler_processes:crawler_processes@localhost/crawler_processes'

    class Config:
        case_sensitive = True


settings: Settings = Settings()
