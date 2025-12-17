from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# URL de conexión: postgresql://usuario:password@host:puerto/nombre_db
DATABASE_URL =  os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True, #verifica conexiones antes de usarlas
    pool_recycle=1800,   # 30 minutos renueva conexiones
    pool_size=5,  #máximo de conexiones en el pool al mismo tiempo
    max_overflow=10, #conexiones extra que se pueden crear si el pool está lleno
    echo=False, #mostrar consultas SQL en consola para depuración
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()