from pydantic import BaseModel
import os

class Settings(BaseModel):
    ORACLE_HOST: str = os.getenv("ORACLE_HOST", "db")
    ORACLE_PORT: int = int(os.getenv("ORACLE_PORT", "1521"))
    ORACLE_SERVICE: str = os.getenv("ORACLE_SERVICE", "XEPDB1")
    ORACLE_USER: str = os.getenv("ORACLE_USER", "LIBRARY")
    ORACLE_PASSWORD: str = os.getenv("ORACLE_PASSWORD", "librarypwd")

    ENV: str = os.getenv("ENV", "dev")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))

settings = Settings()
