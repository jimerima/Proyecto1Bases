from neo4j import GraphDatabase
from utils import read_csv
from persona import add_personas, add_persona, get_persona, update_persona
from club import add_clubs, add_club, get_club, update_club
from autor import add_autores, add_autor, get_autor, update_autor
from libro import add_libros, add_libro, get_libro, update_libro
from membresia import add_membresias, add_membresia
from autoria import add_autorias, add_autoria
from lectura import add_lecturas, add_lectura
from recomendacion import add_recomendaciones, add_recomendacion


URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password")
DATABASE = "proyecto1"

"""
Fabián: 
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
DATABASE = "dbtest2"

Jimena: 
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password")
DATABASE = "proyecto1"
"""

def initialize_db(driver):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("CREATE CONSTRAINT persona_id_unique IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE")
        session.run("CREATE CONSTRAINT club_id_unique IF NOT EXISTS FOR (c:Club) REQUIRE c.idClub IS UNIQUE")
        session.run("CREATE CONSTRAINT autor_id_unique IF NOT EXISTS FOR (a:Autor) REQUIRE a.idAutor IS UNIQUE")
        session.run("CREATE CONSTRAINT libro_id_unique IF NOT EXISTS FOR (l:Libro) REQUIRE l.idLibro IS UNIQUE")


def cargar_datos(driver): 
    initialize_db(driver)
    try:
        personas = read_csv("CSV/Persona.csv")
        clubs = read_csv("CSV/Club.csv")
        autores = read_csv("CSV/Autor.csv")
        libros = read_csv("CSV/Libro.csv")
        membresias = read_csv("CSV/Persona-club.csv")
        autorias = read_csv("CSV/Autor-libro.csv")
        lecturas = read_csv("CSV/Persona-libro.csv")
        recomendaciones = read_csv("CSV/Club-libro.csv")

        add_personas(driver, personas)
        add_clubs(driver, clubs)
        add_autores(driver, autores)
        add_libros(driver, libros)
        add_membresias(driver, membresias)
        add_autorias(driver, autorias)
        add_lecturas(driver, lecturas)
        add_recomendaciones(driver, recomendaciones)

    finally:
        driver.close()
