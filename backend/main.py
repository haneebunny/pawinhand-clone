from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 서버가 살아있는지 확인하는 창구
@app.get("/")
def health_check():
    return {"status": "ok", "message": "백엔드 서버 정상 작동 중"}