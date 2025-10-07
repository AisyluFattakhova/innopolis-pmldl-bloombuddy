from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import chat, scan


app = FastAPI(title="BloomBuddy API")

# Разрешаем запросы с фронтенда
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить до http://localhost:3000
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(chat.router)
app.include_router(scan.router)

@app.get("/")
def root():
    return {"message": "BloomBuddy backend is running 🌱"}
