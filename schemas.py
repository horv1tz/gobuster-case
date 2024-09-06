from pydantic import BaseModel
from typing import List

# Схема для модели Path
class PathBase(BaseModel):
    id: int
    host_id: int
    path: str
    size: int
    status: int

    class Config:
        from_attributes = True  # Включение поддержки работы с моделями SQLAlchemy

# Схема для модели Host
class HostBase(BaseModel):
    id: int
    name: str
    paths: List[PathBase] = []  # Включаем связанные пути в схему хоста

    class Config:
        from_attributes = True  # Включение поддержки работы с моделями SQLAlchemy
