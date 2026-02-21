"""
임베딩 생성 서비스
sentence-transformers를 사용한 다국어 임베딩
"""
from sentence_transformers import SentenceTransformer
from typing import List
from app.config import settings
import hashlib


class EmbeddingService:
    """
    임베딩 생성 및 캐싱 서비스
    - 로컬 실행 가능한 다국어 모델 사용
    - 메모리 캐싱으로 중복 계산 방지
    """
    
    def __init__(self):
        print(f"임베딩 모델 로드 중: {settings.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
        self.cache = {}  # 간단한 메모리 캐시
        print("임베딩 모델 로드 완료")
    
    def _get_cache_key(self, text: str) -> str:
        """텍스트의 캐시 키 생성"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    async def get_embedding(self, text: str) -> List[float]:
        """
        텍스트의 임베딩 벡터 생성
        
        Args:
            text: 임베딩할 텍스트
            
        Returns:
            임베딩 벡터 (384차원)
        """
        cache_key = self._get_cache_key(text)
        
        # 캐시 확인
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        # 임베딩 생성
        embedding = self.model.encode(text, normalize_embeddings=True).tolist()
        
        # 캐시 저장
        self.cache[cache_key] = embedding
        
        return embedding
    
    async def get_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """
        여러 텍스트의 임베딩을 배치로 생성
        
        Args:
            texts: 임베딩할 텍스트 리스트
            
        Returns:
            임베딩 벡터 리스트
        """
        # 캐시되지 않은 텍스트만 필터링
        uncached_texts = []
        uncached_indices = []
        results = [None] * len(texts)
        
        for i, text in enumerate(texts):
            cache_key = self._get_cache_key(text)
            if cache_key in self.cache:
                results[i] = self.cache[cache_key]
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)
        
        # 캐시되지 않은 텍스트들을 배치로 처리
        if uncached_texts:
            embeddings = self.model.encode(
                uncached_texts, 
                normalize_embeddings=True
            ).tolist()
            
            # 결과 저장 및 캐싱
            for i, embedding in zip(uncached_indices, embeddings):
                cache_key = self._get_cache_key(texts[i])
                self.cache[cache_key] = embedding
                results[i] = embedding
        
        return results


# 전역 임베딩 서비스 인스턴스
embedding_service = EmbeddingService()
