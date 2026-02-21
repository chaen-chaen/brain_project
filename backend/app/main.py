"""
FastAPI 메인 애플리케이션
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import notes, recall, graph

# FastAPI 앱 생성
app = FastAPI(
    title="인지 확장 앱 API",
    description="LLM 기반 장기 인지 확장 장치 - 메모를 던지고, 재등장시키는 시스템",
    version="0.1.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API 라우터 등록
app.include_router(notes.router)
app.include_router(recall.router)
app.include_router(graph.router)


@app.get("/")
async def root():
    """헬스 체크 엔드포인트"""
    return {
        "status": "ok",
        "message": "인지 확장 앱 API가 실행 중입니다",
        "version": "0.1.0"
    }


@app.get("/health")
async def health_check():
    """상세 헬스 체크"""
    return {
        "status": "healthy",
        "database": "connected",
        "embedding_model": settings.EMBEDDING_MODEL
    }
