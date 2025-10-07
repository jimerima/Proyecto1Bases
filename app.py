from flask import Flask, render_template, request, redirect, url_for, flash
from main import cargar_datos 
from persona import add_persona, get_persona, update_persona
from autor import add_autor, get_autor, update_autor
from club import add_club, get_club, update_club
from libro import add_libro, get_libro, update_libro
from neo4j import GraphDatabase

app = Flask(__name__)
app.secret_key = "dev"

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
DATABASE = "Proyecto1"

"""
Fabián: 
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
DATABASE = "dbtest2"

Jimena: 
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password")
DATABASE = "proyecto1"

Brandon:
URI = "neo4j://127.0.0.1:7687"
AUTH = ("neo4j", "password")
DATABASE = "proyecto1"
"""

driver = GraphDatabase.driver(URI, auth=AUTH, database=DATABASE)

# ================== RUTAS ==================

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/cargar-datos", methods=["POST"])
def ruta_cargar_datos():
    try:
        cargar_datos(driver)
        return redirect(url_for("pagina_principal"))
    except Exception as e:
        flash(f"Error cargando datos: {e}")
        return redirect(url_for("index"))

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


# Opciones de agregar y modificar

#AUTORES

# --- Autores: listar (con botones Agregar/Modificar) ---

# --- Autores: agregar ---
@app.route("/autores/agregar", methods=["GET", "POST"])
def vista_agregar_autor():
    if request.method == "POST":
        # TODO: leer campos del form y guardar
        # nombre = request.form.get("nombre")
        # apellidos = request.form.get("apellidos")
        # nacionalidad = request.form.get("nacionalidad")
        # fecha_nacimiento = request.form.get("fecha_nacimiento")
        # guardar_autor(...)
        flash("Autor agregado correctamente.", "success")
        return redirect(url_for("vista_autores"))
    return render_template("agregar_autor.html")

# --- Autores: modificar ---
@app.route("/autores/modificar", methods=["GET", "POST"])
def vista_modificar_autor():
    if request.method == "POST":
        # TODO: leer id y campos a actualizar
        # id_autor = request.form.get("id_autor")
        # nombre = request.form.get("nombre")
        # ...
        # actualizar_autor(id_autor, ...)
        flash("Autor modificado correctamente.", "success")
        return redirect(url_for("vista_autores"))
    # En GET podrías recibir ?id= y precargar datos si quieres
    return render_template("modificar_autor.html")

# PERSONA

@app.route("/persona/agregar", methods=["GET","POST"], endpoint="vista_agregar_persona")
def persona_agregar():
    if request.method == "POST":
        # TODO: leer y guardar
        # idp  = request.form.get("id_persona")
        # nom  = request.form.get("nombre")
        # apes = request.form.get("apellidos")
        # corr = request.form.get("correo")
        # tel  = request.form.get("telefono")
        # nac  = request.form.get("fecha_nacimiento")
        # guardar_persona(...)
        flash("Persona agregada correctamente.", "success")
        return redirect(url_for("vista_persona"))
    return render_template("agregar_persona.html")

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
