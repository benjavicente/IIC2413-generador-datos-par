import sqlmodel
import sqlalchemy_utils
from sqlmodel import Session, select
from sqlmodel.main import SQLModel

from .schema import (
    Genero,
    Proveedor,
    Subgenero,
    Videojuego,
    Proveedor_Videojuego,
    Videojuego_Genero,
)


def start(url: str = "sqlite:///games.db", delete_if_exists: bool = False):
    if delete_if_exists and sqlalchemy_utils.database_exists(url):
        sqlalchemy_utils.drop_database(url)
    engine = sqlmodel.create_engine(url)
    SQLModel.metadata.create_all(engine)
    return engine
