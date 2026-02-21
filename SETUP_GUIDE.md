# 🚀 실행 가이드

## Docker 없이 실행하기 (로컬 PostgreSQL 사용)

Docker가 설치되지 않은 경우, 다음 방법으로 실행할 수 있습니다:

### 옵션 1: PostgreSQL 직접 설치

1. **PostgreSQL 설치**
   - https://www.postgresql.org/download/windows/ 에서 설치
   - 설치 시 포트: 5432, 사용자명/비밀번호 설정

2. **pgvector 확장 설치**
   ```bash
   # PostgreSQL에 접속 후
   CREATE EXTENSION vector;
   ```

3. **데이터베이스 생성**
   ```bash
   # psql에서
   CREATE DATABASE brain_db;
   CREATE USER brain_user WITH PASSWORD 'brain_pass';
   GRANT ALL PRIVILEGES ON DATABASE brain_db TO brain_user;
   ```

4. **Backend .env 파일 수정**
   ```
   DATABASE_URL=postgresql://brain_user:brain_pass@localhost:5432/brain_db
   ```

### 옵션 2: SQLite로 임시 실행 (개발용)

pgvector 없이 기본 기능만 테스트하려면:

1. Backend 코드 일부 수정 필요 (pgvector 대신 메모리 기반 검색)

### 옵션 3: Docker Desktop 설치 (권장)

1. **Docker Desktop 설치**
   - https://www.docker.com/products/docker-desktop/ 에서 다운로드
   - 설치 후 재시작

2. **데이터베이스 실행**
   ```bash
   docker compose up -d
   ```

---

## 📝 빠른 시작 (Docker 설치 후)

### 1. 데이터베이스 실행
```bash
cd c:\Users\Admin\brain_project
docker compose up -d
```

### 2. Backend 실행
```bash
cd backend
pip install -r requirements.txt
python init_db.py
uvicorn app.main:app --reload
```

### 3. Frontend 실행
```bash
cd frontend
npm install
npm run dev
```

### 4. 브라우저에서 열기
http://localhost:5173

---

## 🧪 테스트 시나리오

### 시나리오 1: 메모 저장 및 자동 연결

1. "메모 저장" 탭에서 다음 메모들을 순서대로 저장:
   ```
   transformer의 attention 메커니즘이 흥미롭다
   GNN의 message passing도 비슷한 개념인 것 같다
   딥러닝에서 그래프 구조가 중요해지고 있다
   오늘 점심은 뭘 먹을까
   ```

2. 각 메모 저장 후 자동 연결 확인
   - "오늘 점심" 메모는 다른 메모와 연결되지 않음
   - AI/딥러닝 관련 메모들은 서로 연결됨

### 시나리오 2: 재등장 테스트

1. "재등장" 탭에서 질문:
   ```
   최근에 AI 구조에 대해 생각한 내용이 있었는데
   ```

2. 관련 메모들이 맥락 묶음으로 재등장하는지 확인

### 시나리오 3: 그래프 시각화

1. "연결 그래프" 탭 열기
2. 메모들이 노드로, 연결이 엣지로 표시되는지 확인
3. 노드 드래그, 줌 기능 테스트

---

## 문제 해결

### 임베딩 모델 다운로드 느림
첫 실행 시 sentence-transformers 모델(약 200MB)을 다운로드합니다.
시간이 걸릴 수 있으니 기다려주세요.

### 포트 충돌
- Backend 포트 변경: `uvicorn app.main:app --reload --port 8001`
- Frontend 포트는 vite.config.ts에서 변경

### pgvector 확장 오류
```bash
# Docker 컨테이너에 접속하여
docker exec -it brain_postgres psql -U brain_user -d brain_db
CREATE EXTENSION vector;
```
