from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from schemas import HostBase  # Импортируем схемы Pydantic
from utils.crud import get_hosts, create_host, delete_host  # Импортируем CRUD функции
from databases.connection import get_db  # Импортируем зависимость для базы данных

# Создаем экземпляр маршрутизатора
router = APIRouter()

# Эндпоинт для получения списка хостов и связанных с ними путей
@router.get("/hosts", response_model=List[HostBase])
def read_hosts(id: Optional[int] = None, query: Optional[str] = None, db: Session = Depends(get_db)):
    return get_hosts(db=db, id=id, query=query)


# Эндпоинт для создания нового хоста
@router.post("/hosts", response_model=HostBase)
def create_host_endpoint(name: str, path: str, size: int, status: int, db: Session = Depends(get_db)):
    return create_host(db=db, name=name, path=path, size=size, status=status)

# Эндпоинт для удаления хоста по ID
@router.delete("/hosts")
def delete_host_endpoint(id: int, db: Session = Depends(get_db)):
    return delete_host(db=db, id=id)
