"""
메모 API 엔드포인트
메모의 생성, 조회 처리
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.note import Note
from app.schemas.note import NoteCreate, NoteResponse, RelatedNote
from app.services.embedding import embedding_service
from app.services.linking import linking_service

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.post("", response_model=NoteResponse, status_code=201)
async def create_note(
    note_data: NoteCreate,
    db: Session = Depends(get_db)
):
    """
    메모 생성 API
    
    처리 흐름:
    1. 원문 저장
    2. 임베딩 생성
    3. 기존 메모들과 유사도 계산
    4. 임계값 이상인 메모와 자동 연결 생성
    5. 연결된 메모 정보와 함께 반환
    """
    # 1. 메모 생성
    new_note = Note(content=note_data.content)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    
    # 2. 임베딩 생성
    embedding = await embedding_service.get_embedding(note_data.content)
    new_note.embedding = embedding
    db.commit()
    
    # 3. 자동 연결 생성
    await linking_service.create_links(db, new_note)
    
    # 4. 연결된 메모 조회
    related = await linking_service.get_related_notes(db, new_note.id)
    
    # 5. 응답 구성
    related_notes = [
        RelatedNote(
            id=r["id"],
            content=r["content"],
            strength=r["strength"],
            created_at=r["created_at"]
        )
        for r in related
    ]
    
    return NoteResponse(
        id=new_note.id,
        content=new_note.content,
        created_at=new_note.created_at,
        related_notes=related_notes
    )


@router.get("/{note_id}", response_model=NoteResponse)
async def get_note(
    note_id: int,
    db: Session = Depends(get_db)
):
    """
    메모 조회 API
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    
    if not note:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다")
    
    # 연결된 메모 조회
    related = await linking_service.get_related_notes(db, note.id)
    
    related_notes = [
        RelatedNote(
            id=r["id"],
            content=r["content"],
            strength=r["strength"],
            created_at=r["created_at"]
        )
        for r in related
    ]
    
    return NoteResponse(
        id=note.id,
        content=note.content,
        created_at=note.created_at,
        related_notes=related_notes
    )
