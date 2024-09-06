from fastapi import FastAPI
from routers import hosts
from databases.connection import engine, Base

app = FastAPI()

# Создание таблиц в базе данных
Base.metadata.create_all(bind=engine)

# Подключаем маршруты из модуля hosts
app.include_router(hosts.router)

if __name__ == "__main__":
    import uvicorn
    # Запускаем сервер на порту 8000 с перезагрузкой при изменении кода
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
