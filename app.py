######################################################################
# Proyecto 1 - Bases de Datos Avanzadas                              #
# Integrantes:                                                       #
# María Jimena Rivera Madrigal (2023066336)                          #
#
#
######################################################################

from flask import Flask, render_template, request, redirect, url_for, flash
from persona import *
from autor import *
from club import *
from libro import *
from membresia import *
from autoria import *
from lectura import *
from recomendacion import *
from neo4j import GraphDatabase
import csv
import io

#------------------------- Configuración de Flask y Neo4j -------------------------

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


# -------------------------------------------------- Rutas --------------------------------------------------

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

#------------------------- HTML -------------------------

# Rutas para vistas principales

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

# Rutas para agregar y modificar

@app.route("/agregarPersona")
def vista_agregar_persona():
    return render_template("agregarPersona.html")

@app.route("/modificarPersona", methods=["GET"])
def vista_modificar_persona():
    personas = listar_personas(driver)
    return render_template("modificarPersona.html", personas=personas)

@app.route("/agregarAutor")
def vista_agregar_autor():
    return render_template("agregarAutor.html")

@app.route("/modificarAutor", methods=["GET"])
def vista_modificar_autor():
    autores = listar_autores(driver)
    return render_template("modificarAutor.html", autores=autores)

@app.route("/agregarLibro")
def vista_agregar_libro():
    return render_template("agregarLibro.html")

@app.route("/modificarLibro", methods=["GET"])
def vista_modificar_libro():    
    libros = listar_libros(driver)
    if libros is None:
        libros = {}
    return render_template("modificarLibro.html", libros=libros)

@app.route("/agregarClub")
def vista_agregar_club():
    return render_template("agregarClub.html")

@app.route("/modificarClub", methods=["GET"])
def vista_modificar_club():    
    clubes = listar_clubs(driver)
    if clubes is None:
        clubes = {}
    return render_template("modificarClub.html", clubes=clubes)

# Rutas para asociaciones (pendiente de implementar la lógica)

@app.route("/Persona-Club", methods=["GET"])
def vista_asociar_persona_a_club():
    # Lógica para la asociación de personas a clubs (pendiente de implementar)
    return render_template("Persona-Club.html")

@app.route("/Persona-Libro", methods=["GET"])
def vista_asociar_persona_a_libro():
    # Lógica para la asociación de personas a libros (pendiente de implementar)
    return render_template("Persona-Libro.html")

@app.route("/Club-Libro", methods=["GET"])
def vista_asociar_club_a_libro():
    # Lógica para la asociación de clubes a libros (pendiente de implementar)
    return render_template("Club-Libro.html")

@app.route("/Autor-Libro", methods=["GET"])
def vista_asociar_autor_a_libro():
    # Lógica para la asociación de autores a libros (pendiente de implementar)
    return render_template("Autor-Libro.html")

# Rutas para consultas (pendiente de implementar la lógica)

@app.route("/consulta1", methods=["GET"])
def vista_consulta1():
    # Lógica para la consulta 1
    return render_template("consulta1.html")

@app.route("/consulta2", methods=["GET"])
def vista_consulta2():
    # Lógica para la consulta 2
    return render_template("consulta2.html")

@app.route("/consulta3", methods=["GET"])
def vista_consulta3():
    # Lógica para la consulta 3
    return render_template("consulta3.html")

@app.route("/consulta4", methods=["GET"])
def vista_consulta4():
    # Lógica para la consulta 4
    return render_template("consulta4.html")

@app.route("/consulta5", methods=["GET"])
def vista_consulta5():
    # Lógica para la consulta 5
    return render_template("consulta5.html")

# -------------------------------------------------- Opciones de agregar y modificar --------------------------------------------------

# ------------------------- Persona -------------------------
# Agregar persona
@app.route("/agregarPersona", methods=["GET", "POST"])
def agregar_persona():
    if request.method == "POST":
        pId = generar_id_persona(driver) 
        pNombre = request.form.get("nombre")
        pTipoLector = request.form.get("tipo_lector")
        
        add_persona(driver, pId, pNombre, pTipoLector)
        
        flash("Persona agregada correctamente con ID: " + pId, "success")
        return redirect(url_for("vista_persona"))
    
    nuevo_id = generar_id_persona(driver)
    
    return render_template("agregarPersona.html", nuevo_id=nuevo_id)

# Modificar persona
@app.route("/modificarPersona", methods=["GET", "POST"])
def modificar_persona():
    if request.method == "POST":
        pId = request.form.get("id")
        pNombre = request.form.get("nombre")
        pTipoLector = request.form.get("tipo_lector")
        
        update_persona(driver, pId, pNombre, pTipoLector)
        
        flash("Persona modificada correctamente con ID: " + pId, "success")
        return redirect(url_for("vista_persona"))
    
    personas = listar_personas(driver)
    return render_template("modificarPersona.html", personas=personas) 

# ------------------------- Autores -------------------------
# Agregar autor
@app.route("/agregarAutor", methods=["GET", "POST"])
def agregar_autor():
    if request.method == "POST":
        aId = generar_id_autor(driver) 
        aNombre = request.form.get("nombre")
        aNacionalidad = request.form.get("nacionalidad")
        
        add_autor(driver, aId, aNombre, aNacionalidad)
        
        flash("Autor agregado correctamente con ID: " + aId, "success")
        return redirect(url_for("vista_autores"))
    
    nuevo_id = generar_id_autor(driver)
    
    return render_template("agregarAutor.html", nuevo_id=nuevo_id)

# Modificar autor
@app.route("/modificarAutor", methods=["GET", "POST"])
def modificar_autor():
    if request.method == "POST":
        aId = request.form.get("id")
        aNombre = request.form.get("nombre")
        aNacionalidad = request.form.get("nacionalidad")
        
        update_autor(driver, aId, aNombre, aNacionalidad)
        
        flash("Autor modificado correctamente con ID: " + aId, "success")
        return redirect(url_for("vista_autores"))
    
    autores = listar_autores(driver)
    return render_template("modificarAutor.html", autores=autores)

#------------------------- Libros -------------------------
# Agregar libro
@app.route("/agregarLibro", methods=["GET", "POST"])
def agregar_libro():
    if request.method == "POST":
        lId = generar_id_libro(driver) 
        lTitulo = request.form.get("titulo")
        lGenero = request.form.get("genero")
        lAnno = request.form.get("anno")
        
        add_libro(driver, lId, lTitulo, lGenero, lAnno) 
        
        flash("Libro agregado correctamente con ID: " + str(lId), "success")
        return redirect(url_for("vista_libros"))

    return render_template("agregarLibro.html", nuevo_id=lId)

# Modificar libro
@app.route("/modificarLibro", methods=["GET", "POST"])
def modificar_libro():
    libros = listar_libros(driver) 
    
    if request.method == "POST":
        lId = request.form.get("id")   
        lTitulo = request.form.get("titulo")
        lGenero = request.form.get("genero")
        lAnno = request.form.get("anno")
        
        update_libro(driver, lId, lTitulo, lGenero, lAnno)
        
        flash("Libro modificado correctamente con ID: " + str(lId), "success")
        return redirect(url_for("vista_libros"))

    return render_template("modificarLibro.html", libros=libros)

##------------------------- Clubes -------------------------
# Agregar club
@app.route("/agregarClub", methods=["GET", "POST"])
def agregar_club():
    if request.method == "POST":
        cId = generar_id_club(driver) 
        cUbicacion = request.form.get("ubicacion") 
        cTematica = request.form.get("tematica")     
        add_club(driver, cId, cUbicacion, cTematica) 
        
        flash("Club agregado correctamente con ID: " + cId, "success")
        return redirect(url_for("vista_clubes"))
    
    nuevo_id = generar_id_club(driver)
    return render_template("agregarClub.html", nuevo_id=nuevo_id)

# Modificar club
@app.route("/modificarClub", methods=["GET", "POST"])
def modificar_club():
    if request.method == "POST":
        cId = request.form.get("id")
        cUbicacion = request.form.get("ubicacion")
        cTematica = request.form.get("tematica")
        
        update_club(driver, cId, cUbicacion, cTematica)
        
        flash("Club modificado correctamente con ID: " + cId, "success")
        return redirect(url_for("vista_clubes"))
    
    clubes = listar_clubs(driver)
    return render_template("modificarClub.html", clubes=clubes)

#-------------------------------------------------- MAIN --------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)
