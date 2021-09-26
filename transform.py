from db.schema import Proveedor
import db
import json
import datetime
import random

from utils.types import DumpElement, Plataform
from utils.enums import AgeRating


def date_str_from_ts(value: float):
    return datetime.date.fromtimestamp(value).isoformat()


def obt_plataformas(data: list[Plataform], session: db.Session):
    terminos = set()
    for plataforma in data:
        if "PC" in plataforma["name"]:
            terminos.add("PC")
        elif "Xbox" in plataforma["name"]:
            terminos.add("Xbox")
        elif "PlayStation" in plataforma["name"]:
            terminos.add("PlayStation")
        elif "Nintendo" in plataforma["name"]:
            terminos.add("Nintendo")

    provedores: list[db.Proveedor] = []
    for termino in terminos:
        statement = db.select(db.Proveedor).where(db.Proveedor.plataforma == termino)
        results = session.exec(statement).fetchall()
        if len(results) == 1:
            provedores.extend(results)
        else:
            provedores.extend(random.sample(results, k=random.randint(1, len(results))))

    return provedores


def add_element(element: DumpElement, session: db.Session):
    juego = db.Videojuego(
        vid=element["id"],
        fecha_de_lanzamiento=date_str_from_ts(element["first_release_date"]),
        titulo=element["name"],
        clasificacion=AgeRating(element["age_ratings"][0]["rating"]).name,
        puntuacion=element["total_rating"],
    )

    for genero in element["themes"]:
        query = db.select(db.Genero).where(db.Genero.gid == genero["id"])
        genero_obj = session.exec(query).first()
        if genero_obj == None:
            genero_obj = db.Genero(gid=genero["id"], nombre=genero["name"])
        juego.generos.append(genero_obj)
    juego.proveedores.extend(obt_plataformas(element["platforms"], session))
    session.add(juego)


def create_providers(s: db.Session):
    s.add(db.Proveedor(prov_id=1, nombre="Epic Games", plataforma="PC"))
    s.add(db.Proveedor(prov_id=2, nombre="Steam", plataforma="PC"))
    s.add(db.Proveedor(prov_id=3, nombre="GOG", plataforma="PC"))
    s.add(db.Proveedor(prov_id=4, nombre="PlayStation Store", plataforma="PlayStation"))
    s.add(db.Proveedor(prov_id=5, nombre="Xbox Games Store", plataforma="Xbox"))
    s.add(db.Proveedor(prov_id=6, nombre="Nintendo eShop", plataforma="Nintendo"))


def main():
    with open("data_dump.json", encoding="utf-8") as file:
        DUMP: list[DumpElement] = json.load(file)

    engine = db.start(delete_if_exists=True)
    with db.Session(engine) as session:
        create_providers(session)

        for element in DUMP:
            if all(k in element.keys() for k in ["age_ratings", "themes"]):
                add_element(element, session)

        session.commit()


if __name__ == "__main__":
    main()
