# 🧠 The Second Brain (인지 확장 앱)

LLM 기반 장기 인지 확장 장치 - 기억을 완전히 맡길 수 있는 나만의 두 번째 뇌 시스템입니다.

## 📖 개요

이 앱은 단순한 메모 앱이 아닙니다. 사용자의 뇌를 도와주는 "장기 인지 확장 장치"로 설계되었습니다:

- ✅ **제목, 폴더, 태그 불필요** - 머릿속에 떠오르는 생각을 그냥 던지듯 저장하세요.
- ✅ **자동 의미 연결** - 시스템이 스스로 메모 간의 의미적 관계를 분석하여 연결을 생성합니다.
- ✅ **자연스러운 재등장 (Recall)** - 검색할 필요가 없습니다. 당신의 사고 흐름에 맞춰 관련 기억이 자연스럽게 호출됩니다.
- ✅ **시각적 통찰** - D3.js 기반의 다이내믹 그래프를 통해 당신의 생각들이 어떻게 엮여 있는지 관찰하세요.

## 🛠 기술 스택

### Backend
- **Python 3.10** (라이브러리 호환성을 위해 권장)
- **FastAPI** - 고성능 비동기 Python 웹 프레임워크
- **PostgreSQL + pgvector** - 의미 기반 검색을 위한 벡터 데이터베이스
- **psycopg (v3)** - 차세대 PostgreSQL 파이썬 어댑터
- **SQLAlchemy** - 강력한 SQL 툴킷 및 ORM
- **sentence-transformers** - 로컬 실행 다국어 임베딩 모델 (`paraphrase-multilingual-MiniLM-L12-v2`)

### Frontend
- **React + TypeScript** - UI 프레임워크
- **Vite** - 빠른 빌드 및 개발 도구
- **D3.js** - 데이터 기반 동적 그래프 시각화
- **Vanilla CSS** - 커스텀 다크 모드 및 프리미엄 디자인 구현

## 🚀 시작하기

### 1. 데이터베이스 실행 (Docker)

```bash
# 프로젝트 루트에서
docker-compose up -d
```
*pgvector가 활성화된 PostgreSQL이 5432 포트에서 실행됩니다.*

### 2. Backend 설정

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
.\venv\Scripts\Activate.ps1

# 의존성 설치
pip install -r requirements.txt

# 데이터베이스 초기화 (pgvector 확장 및 테이블 생성)
python init_db.py

# 서버 실행
uvicorn app.main:app --reload
```
*API 서버는 http://localhost:8000 에서 실행됩니다.*

### 3. Frontend 설정

```bash
cd frontend

# 의존성 설치
npm install

# 개발 서버 실행
npm run dev
```
*웹 앱은 http://localhost:5173 에서 실행됩니다.*

## 🎨 디자인 철학

### "기억의 숲 (Forest of Memories)" 테마
- **뉴트럴 다크 모드**: 푸른 기를 뺀 순수 진회색 배경으로 눈의 피로를 최소화하고 집중력을 높였습니다.
- **에메랄드 그린 포인트**: 유기적인 성장과 정신적 활력을 상징하는 초록색을 메인 컬러로 사용했습니다.
- **차분한 입력창**: 너무 밝지 않은 유회색(Soft Gray) 입력창을 통해 편안한 기록 경험을 제공합니다.
- **인간공학적 레이아웃**: 주요 액션 버튼을 우측에 배치하여 직관적인 조작이 가능하도록 했습니다.

## 💡 주요 기능

### 1. Just Cast (Input 탭)
- 제목을 고민하지 마세요. 그냥 타이핑하고 저장하세요.
- 시스템이 실시간으로 "자동 연결된 메모"를 찾아 보여줍니다.

### 2. Inquire and Ignite (Recall 탭)
- 질문이나 현재 하고 있는 생각을 입력해 보세요.
- 과거의 기억들이 "의미 클러스터(묶음)" 형태로 유사도 점수와 함께 재등장합니다.

### 3. Observe the Connections (Graph 탭)
- 당신만의 지식 네트워크를 시각적으로 확인하세요.
- 노드의 크기와 선의 굵기가 기억의 중요도와 연결 강도를 나타냅니다.
- Refresh를 눌러 성장해가는 당신의 뇌를 관찰하세요.

## ⚙️ 설정 (.env)

`backend/.env`를 통해 시스템을 튜닝할 수 있습니다:
```ini
DATABASE_URL=postgresql+psycopg://brain_user:brain_pass@localhost:5432/brain_db
SIMILARITY_THRESHOLD=0.7  # 메모 간 연결 생성 임계값
CORS_ORIGINS=http://localhost:5173
```

## 📜 설계 원칙

> **"기억을 잘하게 돕는 앱"이 아니라 "기억을 맡길 수 있는 앱"**

1. **사용자 부담 최소화** - 모든 조직화(Organization)는 시스템의 몫입니다.
2. **자동화된 연결** - 맥락은 사용자가 만드는 것이 아니라 시스템이 발견하는 것입니다.
3. **재등장 중심** - "검색"하지 마세요. 당신의 사고에 맞춰 시스템이 기억을 "제시"할 것입니다.

## 📝 라이센스

MIT
