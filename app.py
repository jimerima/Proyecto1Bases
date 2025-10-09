from flask import Flask, render_template, request, redirect, url_for, flash
from persona import *
from autor import add_autor, get_autor, update_autor, add_autores
from club import add_club, get_club, update_club, add_clubs
from libro import add_libro, get_libro, update_libro, add_libros
from membresia import add_membresia, add_membresias
from autoria import add_autoria, add_autorias
from lectura import add_lectura, add_lecturas
from recomendacion import add_recomendacion, add_recomendaciones
from neo4j import GraphDatabase
import csv
import io

app = Flask(__name__)
app.secret_key = "dev"

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
DATABASE = "proyecto1"


driver = GraphDatabase.driver(URI, auth=AUTH, database=DATABASE)

def initialize_db(driver):
    with driver.session() as session:
        session.run("MATCH (n) DETACH DELETE n")
        session.run("CREATE CONSTRAINT persona_id_unique IF NOT EXISTS FOR (p:Persona) REQUIRE p.id IS UNIQUE")
        session.run("CREATE CONSTRAINT club_id_unique IF NOT EXISTS FOR (c:Club) REQUIRE c.idClub IS UNIQUE")
        session.run("CREATE CONSTRAINT autor_id_unique IF NOT EXISTS FOR (a:Autor) REQUIRE a.idAutor IS UNIQUE")
        session.run("CREATE CONSTRAINT libro_id_unique IF NOT EXISTS FOR (l:Libro) REQUIRE l.idLibro IS UNIQUE")


# ================== RUTAS ==================

@app.route("/")
def index():
    initialize_db(driver)
    return render_template("index.html")

@app.route("/cargar-datos", methods=["POST"])
def ruta_cargar_datos():
    datos = request.files.getlist("datos")
        
    if not datos:
        flash("No se seleccionaron archivos.", "error")
        return redirect(url_for("index"))

    NODE_FILES = {"Persona.csv", "Club.csv", "Autor.csv", "Libro.csv"}
    REL_FILES  = {"Persona-club.csv", "Autor-libro.csv", "Persona-libro.csv", "Club-libro.csv"}
    KNOWN = NODE_FILES | REL_FILES

    ok, unknown = [], []
    parsed = [] 

    for archivo in datos:
        nombre = archivo.filename.strip()
        if nombre not in KNOWN:
            unknown.append(nombre)
            continue
        texto = io.TextIOWrapper(archivo.stream, encoding="utf-8-sig", newline="")
        reader = csv.DictReader(texto, delimiter=";")
        data_list = list(reader)
        parsed.append((nombre, data_list))

    
    def dispatch(nombre, data_list):
        match nombre:
            case "Persona.csv":         add_personas(driver, data_list)
            case "Club.csv":            add_clubs(driver, data_list)
            case "Autor.csv":           add_autores(driver, data_list)
            case "Libro.csv":           add_libros(driver, data_list)
            case "Persona-club.csv":    add_membresias(driver, data_list)
            case "Autor-libro.csv":     add_autorias(driver, data_list)
            case "Persona-libro.csv":   add_lecturas(driver, data_list)
            case "Club-libro.csv":      add_recomendaciones(driver, data_list)

    
    for nombre, data_list in parsed:
        if nombre in NODE_FILES:
            try:
                dispatch(nombre, data_list)
                ok.append(f"{nombre}: {len(data_list)} registros cargados.")
            except Exception as e:
                flash(f"Error cargando {nombre}: {e}", "error")


    for nombre, data_list in parsed:
        if nombre in REL_FILES:
            try:
                dispatch(nombre, data_list)
                ok.append(f"{nombre}: {len(data_list)} registros cargados.")
            except Exception as e:
                flash(f"Error cargando {nombre}: {e}", "error")

    if not ok:
        flash("No se cargaron archivos válidos.", "error")
        return redirect(url_for("index"))
    if ok:
        flash("Archivos cargados:\n" + "\n".join(ok), "success")
    if unknown:
        flash("Archivos no reconocidos:\n" + "\n".join(unknown), "error")
    

    return redirect(url_for("pagina_principal")) 


@app.route("/PaginaPrincipal")
def pagina_principal():
    return render_template("PaginaPrincipal.html")

@app.route("/autores")
def vista_autores():
    return render_template("autores.html")

@app.route("/libros")
def vista_libros():
    return render_template("libros.html")

@app.route("/clubes")
def vista_clubes():
    return render_template("clubes.html")

@app.route("/asociacion")
def vista_asociacion():
    return render_template("asociacion.html")

@app.route("/consultas")
def vista_consultas():
    return render_template("consultas.html")

@app.route("/persona")
def vista_persona():
    return render_template("persona.html")

@app.route("/agregarPersona")
def vista_agregar_persona():
    return render_template("agregarPersona.html")

# ------------------------- Opciones de agregar y modificar -------------------------


# PERSONA

@app.route("/agregarPersona", methods=["GET", "POST"])
def agregar_persona():
    if request.method == "POST":
        pId = request.form.get("id_persona")
        pNombre = request.form.get("nombre")
        pTipoLector = request.form.get("tipo_lector")
        add_persona(driver, pId, pNombre, pTipoLector)
        flash("Persona agregada correctamente.", "success")
        return redirect(url_for("vista_persona"))
    
    nuevo_id = generar_id_persona(driver)
    
    return render_template("agregarPersona.html", nuevo_id=nuevo_id)


@app.route("/persona/modificar", methods=["GET","POST"], endpoint="vista_modificar_persona")
def persona_modificar():
    if request.method == "POST":
        # TODO: leer y actualizar
        # idp  = request.form.get("id_persona")
        # nom  = request.form.get("nombre")
        # apes = request.form.get("apellidos")
        # corr = request.form.get("correo")
        # tel  = request.form.get("telefono")
        # nac  = request.form.get("fecha_nacimiento")
        # actualizar_persona(idp, ...)
        flash("Persona modificada correctamente.", "success")
        return redirect(url_for("vista_persona"))
    return render_template("modificar_persona.html")


# ================== MAIN ==================
if __name__ == "__main__":
    app.run(debug=True)
