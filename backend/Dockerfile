# 1. 파이썬 3.10 환경 사용
FROM python:3.10

# 2. 컨테이너 내부 작업 디렉토리 설정
WORKDIR /app

# 3. 라이브러리 설치를 위한 파일 복사
COPY requirements.txt .

# 4. 라이브러리 설치 (메모리 부족 방지를 위해 캐시 없이 설치)
RUN pip install --no-cache-dir -r requirements.txt

# 5. 나머지 소스 코드 전체 복사
COPY . .

# 6. FastAPI 서버 실행 (0.0.0.0으로 열어야 외부 접속 가능)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]