# 1. 노드(Node.js) 환경 사용
FROM node:20

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 패키지 목록 복사 및 설치
COPY package*.json ./
RUN npm install

# 4. 소스 코드 복사
COPY . .

# 5. Vite 개발 서버 실행 (host 설정을 해야 외부에서 접속됨)
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]