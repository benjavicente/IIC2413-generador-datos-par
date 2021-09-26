import json
import datetime
import random
import math

import db

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


def crear_generos(element: DumpElement, juego: db.Videojuego, session: db.Session):
    contador_genero = len(session.exec(db.select(db.Genero)).fetchall())
    posibles_generos = element["genres"] + element["themes"]
    generos_maximos = max(2, round(math.log2(len(posibles_generos))))
    cantidad_generos = random.randrange(1, generos_maximos)
    for genero in random.sample(posibles_generos, k=cantidad_generos):
        query = db.select(db.Genero).where(db.Genero.nombre == genero["name"])
        genero_obj = session.exec(query).first()
        if genero_obj == None:
            genero_obj = db.Genero(gid=contador_genero, nombre=genero["name"])
            session.add(genero_obj)
            contador_genero += 1
        juego.generos.append(genero_obj)

def add_element(element: DumpElement, session: db.Session):
    juego = db.Videojuego(
        vid=element["id"],
        fecha_de_lanzamiento=date_str_from_ts(element["first_release_date"]),
        titulo=element["name"],
        clasificacion=AgeRating(element["age_ratings"][0]["rating"]).name,
        puntuacion=element["total_rating"],
    )
    crear_generos(element, juego, session)
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
    genero_subgeneros = {
        "FPS": ["Warfare", "Survival"],
        "Strategy": ["Turn-based strategy (TBS)", "Real Time Strategy (RTS)"],
        "Simulator": ["Role-playing (RPG)"],
        "Action": ["Adventure", "FPS", "Hack and slash/Beat 'em up"],
        "Adventure": ["Open world", "Role-playing (RPG)"],
        "Survival": ["Horror"],
        "Mystery": ["Horror", "Thriller"]
    }

    with open("data_dump.json", encoding="utf-8") as file:
        dump: list[DumpElement] = json.load(file)

    engine = db.start(delete_if_exists=True)
    with db.Session(engine) as session:
        create_providers(session)

        for element in dump[:120]:
            if all(k in element.keys() for k in ["age_ratings", "themes"]):
                add_element(element, session)

        query = db.select(db.Genero).where(db.Genero.nombre == "Shooter")
        session.exec(query).one().nombre = "FPS"

        for genero, subgeneros in genero_subgeneros.items():
            query = db.select(db.Genero).where(db.Genero.nombre == genero)
            genero_obj = session.exec(query).first()
            if not genero_obj:
                continue

            for subgenero in subgeneros:
                query = db.select(db.Genero).where(db.Genero.nombre == subgenero)
                subgenero_obj = session.exec(query).first()
                if not subgenero_obj:
                    continue

                session.add(db.Subgenero(gid=genero_obj.gid, sub_gid=subgenero_obj.gid))

        session.commit()


if __name__ == "__main__":
    main()

    # import pprint
    # engine = db.start()
    # with db.Session(engine) as session:
    #     print("\nGeneros y su cantidad de juegos")
    #     for genero in session.exec(db.select(db.Genero)):
    #         print(f"{len(genero.videojuegos):>5} - {genero.nombre}")
    #     print("\nProvedores y su cantidad de juegos")
    #     for proveedor in session.exec(db.select(db.Proveedor)):
    #         print(f"{len(proveedor.videojuegos):>5} - {proveedor.nombre}")

        # orden = db.Videojuego.puntuacion.desc()
        # print("Consulta 1")
        # resultados = session.exec(db.select(db.Videojuego).order_by(orden))
        # for juego in resultados.fetchmany(10):
        #     pprint.pprint({
        #         "juego": juego,
        #         "proveedores": [p.nombre for p in juego.proveedores],
        #     })

        # # Consulta 2
        # # no hay reseñas aún :(

        # print("Consulta 3")
        # query = db.select(db.Videojuego, db.Genero, db.Videojuego_Genero).where(
        #     db.Genero.gid == db.Videojuego_Genero.gid,
        #     db.Videojuego.vid == db.Videojuego_Genero.vid,
        #     db.Genero.nombre == "FPS"
        # )
        # resultados = session.exec(query)
        # for juego, genero, _ in resultados.fetchmany(10):
        #     pprint.pprint({
        #         "juego": juego.titulo,
        #         "genero": genero.nombre,
        #     })
