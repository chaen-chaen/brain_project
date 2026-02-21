"""
애플리케이션 설정 관리
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """환경 변수 기반 설정"""
    
    # 데이터베이스
    DATABASE_URL: str = "postgresql+psycopg://brain_user:brain_pass@localhost:5432/brain_db"
    
    # 임베딩 모델
    EMBEDDING_MODEL: str = "paraphrase-multilingual-MiniLM-L12-v2"
    EMBEDDING_DIMENSION: int = 384
    
    # 자동 연결 임계값
    SIMILARITY_THRESHOLD: float = 0.7
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:5173,http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """CORS origins를 리스트로 반환"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 전역 설정 인스턴스
settings = Settings()
