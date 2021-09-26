from typing import TypedDict


class AgeRating(TypedDict):
    id: int
    category: int
    rating: int


class Plataform(TypedDict):
    id: int
    name: str
    plataform_familly: "Plataform"


class Theme(TypedDict):
    id: int
    name: str


class DumpElement(TypedDict):
    id: int
    age_ratings: list[AgeRating]
    name: str
    platforms: list[Plataform]
    summarry: str
    themes: list[Theme]
    genres: list[Theme]
    total_rating: float
    first_release_date: float
