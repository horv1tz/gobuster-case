from sqlalchemy.orm import Session
from fastapi import HTTPException

from databases.models import Host, Path

# Функция для получения списка хостов или одного хоста по ID/запросу
def get_hosts(db: Session, id: int = None, query: str = None):
    if id:
        # Поиск хоста по ID с подгрузкой связанных путей
        host = db.query(Host).filter(Host.id == id).first()
        if not host:
            raise HTTPException(status_code=404, detail="Host not found")
        return [host]
    elif query:
        # Поиск хостов по запросу с подгрузкой связанных путей
        hosts = db.query(Host).filter(Host.name.like(f"%{query}%")).all()
        if not hosts:
            raise HTTPException(status_code=404, detail="No hosts found")
        return hosts
    else:
        # Получение всех хостов с подгрузкой связанных путей
        return db.query(Host).all()


# Функция для создания нового хоста и пути
def create_host(db: Session, name: str, path: str, size: int, status: int):
    # Создание нового хоста
    new_host = Host(name=name)
    db.add(new_host)
    db.commit()
    db.refresh(new_host)

    # Создание нового пути для хоста
    new_path = Path(host_id=new_host.id, path=path, size=size, status=status)
    db.add(new_path)
    db.commit()
    db.refresh(new_path)

    return new_host

# Функция для удаления хоста и связанных с ним путей
def delete_host(db: Session, id: int):
    # Поиск хоста по ID
    host = db.query(Host).filter(Host.id == id).first()
    if not host:
        raise HTTPException(status_code=404, detail="Host not found")

    # Удаление всех путей, связанных с хостом
    db.query(Path).filter(Path.host_id == id).delete()

    # Удаление хоста
    db.delete(host)
    db.commit()

    return {"id": id}
