"""
재등장(Recall) 서비스
질문에 대해 과거 메모를 의미 기반으로 재등장시킴
"""
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict
from datetime import datetime
import math
from app.services.embedding import embedding_service


class RecallService:
    """
    재등장 서비스
    - 단순 검색이 아닌 "재등장" 개념
    - 의미 유사도 + 시간 가중치
    - 연결된 메모를 맥락 묶음으로 반환
    """
    
    async def recall(
        self, 
        db: Session, 
        query: str, 
        limit: int = 10
    ) -> List[Dict]:
        """
        질문에 대한 메모 재등장
        
        Args:
            db: 데이터베이스 세션
            query: 질문 또는 사고 내용
            limit: 최대 반환 개수
            
        Returns:
            맥락 묶음 리스트
        """
        # 1. 질문 임베딩 생성
        query_embedding = await embedding_service.get_embedding(query)
        
        # 2. 유사도 + 시간 가중치로 관련 메모 검색
        # 시간 가중치 공식: 1 + log(days_ago + 1) * 0.1
        # 오래된 메모라도 의미가 강하면 노출
        search_query = text("""
            SELECT 
                id,
                content,
                created_at,
                embedding,
                (1 - (embedding <=> :embedding)) * 
                (1 + log(EXTRACT(EPOCH FROM (NOW() - created_at)) / 86400 + 1) * 0.1) as relevance_score
            FROM notes
            WHERE embedding IS NOT NULL
            ORDER BY relevance_score DESC
            LIMIT :limit
        """)
        
        result = db.execute(
            search_query,
            {
                "embedding": str(query_embedding),
                "limit": limit * 2  # 클러스터링을 위해 더 많이 가져옴
            }
        )
        
        recalled_notes = []
        for row in result.fetchall():
            recalled_notes.append({
                "id": row.id,
                "content": row.content,
                "created_at": row.created_at,
                "relevance_score": float(row.relevance_score)
            })
        
        # 3. 연결된 메모들을 클러스터로 묶기
        clusters = await self._cluster_notes(db, recalled_notes, limit)
        
        return clusters
    
    async def _cluster_notes(
        self, 
        db: Session, 
        notes: List[Dict], 
        max_notes: int
    ) -> List[Dict]:
        """
        연결된 메모들을 맥락 묶음으로 클러스터링
        
        Args:
            db: 데이터베이스 세션
            notes: 재등장한 메모 리스트
            max_notes: 최대 메모 개수
            
        Returns:
            클러스터 리스트
        """
        if not notes:
            return []
        
        # 메모 ID 리스트
        note_ids = [note["id"] for note in notes]
        
        # 메모 간 연결 정보 조회
        links_query = text("""
            SELECT source_note_id, target_note_id, strength
            FROM memory_links
            WHERE source_note_id = ANY(:note_ids)
                AND target_note_id = ANY(:note_ids)
                AND strength >= 0.75
        """)
        
        result = db.execute(links_query, {"note_ids": note_ids})
        links = result.fetchall()
        
        # 연결 그래프 구축
        graph = {note_id: [] for note_id in note_ids}
        for link in links:
            graph[link.source_note_id].append(link.target_note_id)
        
        # 연결된 메모들을 그룹핑 (간단한 BFS 기반 클러스터링)
        visited = set()
        clusters = []
        
        for note in notes[:max_notes]:
            if note["id"] in visited:
                continue
            
            # BFS로 연결된 메모 찾기
            cluster_notes = []
            queue = [note["id"]]
            cluster_visited = set()
            
            while queue:
                current_id = queue.pop(0)
                if current_id in cluster_visited:
                    continue
                
                cluster_visited.add(current_id)
                visited.add(current_id)
                
                # 현재 메모 추가
                current_note = next((n for n in notes if n["id"] == current_id), None)
                if current_note:
                    cluster_notes.append(current_note)
                
                # 연결된 메모 탐색 (깊이 1까지만)
                if len(cluster_notes) < 5:  # 클러스터 크기 제한
                    for connected_id in graph.get(current_id, []):
                        if connected_id not in cluster_visited:
                            queue.append(connected_id)
            
            if cluster_notes:
                # 클러스터 이유 생성 (간단하게 첫 메모의 키워드)
                cluster_reason = self._extract_cluster_reason(cluster_notes)
                clusters.append({
                    "cluster_reason": cluster_reason,
                    "notes": cluster_notes
                })
        
        return clusters
    
    def _extract_cluster_reason(self, notes: List[Dict]) -> str:
        """
        클러스터의 주제/이유 추출
        
        Args:
            notes: 클러스터에 속한 메모들
            
        Returns:
            클러스터 이유 문자열
        """
        # 간단한 구현: 첫 메모의 앞부분 사용
        # 추후 LLM으로 주제 요약 가능
        if not notes:
            return "관련 메모"
        
        first_content = notes[0]["content"]
        if len(first_content) > 30:
            return first_content[:30] + "..."
        return first_content


# 전역 재등장 서비스 인스턴스
recall_service = RecallService()
