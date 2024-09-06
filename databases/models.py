from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from databases.connection import Base

# Модель таблицы "hosts"
class Host(Base):
    __tablename__ = 'hosts'  # Название таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ
    name = Column(String, nullable=False)  # Название хоста
    paths = relationship("Path", back_populates="host")  # Связь с таблицей "paths"

# Модель таблицы "paths"
class Path(Base):
    __tablename__ = 'paths'  # Название таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)  # Первичный ключ
    host_id = Column(Integer, ForeignKey('hosts.id'))  # Внешний ключ для связи с таблицей "hosts"
    path = Column(String, nullable=False)  # Путь
    size = Column(Integer)  # Размер
    status = Column(Integer)  # Статус
    host = relationship("Host", back_populates="paths")  # Связь с таблицей "hosts"
