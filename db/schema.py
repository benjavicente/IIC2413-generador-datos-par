from typing import Optional, List
from sqlmodel import Field, SQLModel
from sqlmodel.main import Relationship


class Proveedor_Videojuego(SQLModel, table=True):
    prov_id: int = Field(foreign_key="proveedor.prov_id", primary_key=True)
    vid: int = Field(foreign_key="videojuego.vid", primary_key=True)


class Subgenero(SQLModel, table=True):
    gid: int = Field(foreign_key="genero.gid", primary_key=True)
    sub_gid: int = Field(foreign_key="genero.gid", primary_key=True)


class Videojuego_Genero(SQLModel, table=True):
    vid: int = Field(foreign_key="videojuego.vid", primary_key=True)
    gid: int = Field(foreign_key="genero.gid", primary_key=True)


class Videojuego(SQLModel, table=True):
    vid: int = Field(default=None, primary_key=True)
    titulo: str
    puntuacion: float
    clasificacion: str
    fecha_de_lanzamiento: str
    # Relation attributes
    generos: List["Genero"] = Relationship(link_model=Videojuego_Genero)
    proveedores: List["Proveedor"] = Relationship(
        back_populates="videojuegos", link_model=Proveedor_Videojuego
    )


class Proveedor(SQLModel, table=True):
    prov_id: int = Field(default=None, primary_key=True)
    nombre: str
    plataforma: str
    # Relation attributes
    videojuegos: List["Videojuego"] = Relationship(
        back_populates="proveedores", link_model=Proveedor_Videojuego
    )


class Genero(SQLModel, table=True):
    gid: int = Field(default=None, primary_key=True)
    nombre: str
    # Relation attributes
    videojuegos: List["Videojuego"] = Relationship(
        back_populates="generos", link_model=Videojuego_Genero
    )
    sub_generos: List["Genero"] = Relationship(
        link_model=Subgenero, sa_relationship_kwargs={"foreign_keys": "Subgenero.gid"}
    )
