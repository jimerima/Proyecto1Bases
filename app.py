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
# ================== MAIN ==================
if __name__ == "__main__":
    app.run(debug=True)
