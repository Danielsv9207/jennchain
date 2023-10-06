from fastapi import FastAPI, HTTPException, Path, status, Depends
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine, Column, Integer, String, Boolean, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import databases


# Configuración de la base de datos
DATABASE_URL = "postgresql://jennchain:jennchain@db/jennchain"

metadata = MetaData()
Base = declarative_base()

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    contacto = Column(String(255), nullable=False, unique=True)
    es_admin = Column(Boolean, default=False)
    
database = databases.Database(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=database)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UsuarioIn(BaseModel):
    nombre: str
    contacto: str
    es_admin: bool = False

class UsuarioOut(UsuarioIn):
    id: int

@app.post("/usuarios/", response_model=UsuarioOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UsuarioIn, db: Session = Depends(get_db)):
    nuevo_usuario = Usuario(**user.dict())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario

@app.get("/usuarios/{user_id}/", response_model=UsuarioOut)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    usuario = db.query(Usuario).filter(Usuario.id == user_id).first()
    if usuario is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return usuario

@app.put("/usuarios/{user_id}/", response_model=UsuarioOut)
async def update_user(user_id: int, user: UsuarioIn, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    for key, value in user.dict().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/usuarios/{user_id}/", response_model=dict)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(Usuario).filter(Usuario.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    db.delete(db_user)
    db.commit()
    return {"message": "Usuario eliminado exitosamente"}

@app.on_event("startup")
async def startup():
    await database.connect()