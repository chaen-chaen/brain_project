"""
자동 연결 생성 서비스
의미 유사도 기반으로 메모 간 연결을 자동 생성
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from app.models.note import Note
from app.models.memory_link import MemoryLink
from app.config import settings


class LinkingService:
    """
    메모 간 자동 연결 서비스
    - pgvector를 사용한 유사도 검색
    - 임계값 이상인 메모들과 자동 연결
    """
    
    async def create_links(
        self, 
        db: Session, 
        new_note: Note, 
        top_k: int = 10
    ) -> List[MemoryLink]:
        """
        새 메모와 기존 메모들 간의 자동 연결 생성
        
        Args:
            db: 데이터베이스 세션
            new_note: 새로 생성된 메모
            top_k: 상위 K개의 유사 메모 검색
            
        Returns:
            생성된 MemoryLink 리스트
        """
        if new_note.embedding is None:
            return []
        
        # pgvector의 코사인 거리로 유사 메모 검색
        # 코사인 거리: 1 - 코사인 유사도
        # 따라서 거리가 작을수록 유사함
        query = text("""
            SELECT 
                id,
                content,
                created_at,
                1 - (embedding <=> CAST(:embedding AS vector)) as similarity
            FROM notes
            WHERE id != :note_id
                AND embedding IS NOT NULL
            ORDER BY embedding <=> CAST(:embedding AS vector)
            LIMIT :limit
        """)
        
        # numpy array인 경우 list로 변환 후 문자열로 직렬화 (pgvector 호환성)
        embedding_value = new_note.embedding
        if hasattr(embedding_value, 'tolist'):
            embedding_value = embedding_value.tolist()
        
        # 리스트를 문자열로 변환 "[1.0, 2.0, ...]"
        embedding_str = str(embedding_value)

        result = db.execute(
            query,
            {
                "embedding": embedding_str,
                "note_id": new_note.id,
                "limit": top_k
            }
        )
        
        similar_notes = result.fetchall()
        
        # 임계값 이상인 메모들과 연결 생성
        created_links = []
        for row in similar_notes:
            similarity = float(row.similarity)
            
            if similarity >= settings.SIMILARITY_THRESHOLD:
                # 양방향 연결 생성
                # 1. new_note -> similar_note
                link1 = MemoryLink(
                    source_note_id=new_note.id,
                    target_note_id=row.id,
                    strength=similarity,
                    reason="semantic similarity"
                )
                db.add(link1)
                created_links.append(link1)
                
                # 2. similar_note -> new_note
                link2 = MemoryLink(
                    source_note_id=row.id,
                    target_note_id=new_note.id,
                    strength=similarity,
                    reason="semantic similarity"
                )
                db.add(link2)
                created_links.append(link2)
        
        db.commit()
        
        return created_links
    
    async def get_related_notes(
        self, 
        db: Session, 
        note_id: int, 
        min_strength: float = 0.0
    ) -> List[dict]:
        """
        특정 메모와 연결된 메모들 조회
        
        Args:
            db: 데이터베이스 세션
            note_id: 메모 ID
            min_strength: 최소 연결 강도
            
        Returns:
            연결된 메모 정보 리스트
        """
        query = text("""
            SELECT 
                n.id,
                n.content,
                n.created_at,
                ml.strength
            FROM notes n
            JOIN memory_links ml ON n.id = ml.target_note_id
            WHERE ml.source_note_id = :note_id
                AND ml.strength >= :min_strength
            ORDER BY ml.strength DESC
        """)
        
        result = db.execute(
            query,
            {"note_id": note_id, "min_strength": min_strength}
        )
        
        related = []
        for row in result.fetchall():
            related.append({
                "id": row.id,
                "content": row.content,
                "created_at": row.created_at,
                "strength": float(row.strength)
            })
        
        return related


# 전역 링킹 서비스 인스턴스
linking_service = LinkingService()
