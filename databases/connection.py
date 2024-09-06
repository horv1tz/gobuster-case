import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Настройка строки подключения к PostgreSQL
# Замените 'username', 'password', 'hostname', 'port', и 'dbname' на реальные данные вашей базы данных
# DATABASE_URL = "postgresql+psycopg2://username:password@hostname:port/dbname"
DATABASE_URL = os.getenv("DATABASE_URL")
# Создаем объект engine для подключения к базе данных
engine = create_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий для управления соединениями с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей базы данных
Base = declarative_base()

# Функция для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
