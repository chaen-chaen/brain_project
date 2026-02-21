"""
Note 관련 Pydantic 스키마
"""
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class NoteCreate(BaseModel):
    """메모 생성 요청"""
    content: str = Field(..., min_length=1, description="메모 내용")


class RelatedNote(BaseModel):
    """연결된 메모 정보"""
    id: int
    content: str
    strength: float = Field(..., ge=0.0, le=1.0, description="연결 강도")
    created_at: datetime
    
    class Config:
        from_attributes = True


class NoteResponse(BaseModel):
    """메모 생성/조회 응답"""
    id: int
    content: str
    created_at: datetime
    related_notes: List[RelatedNote] = []
    
    class Config:
        from_attributes = True


class NoteDetail(BaseModel):
    """메모 상세 정보"""
    id: int
    content: str
    created_at: datetime
    
    class Config:
        from_attributes = True
