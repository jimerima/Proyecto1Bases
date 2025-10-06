from flask import Flask, render_template, request
from main import cargar_datos 
from persona import add_persona, get_persona, update_persona
from autor import add_autor, get_autor, update_autor
from club import add_club, get_club, update_club
from libro import add_libro, get_libro, update_libro
from neo4j import GraphDatabase

app = Flask(__name__)

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
DATABASE = "Proyecto1"

driver = GraphDatabase.driver(URI, auth=AUTH, database=DATABASE)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/load_data')
def load_data():
    cargar_datos(driver) 
    return "Datos cargados exitosamente."

@app.route('/personas', methods=['GET', 'POST'])
def personas():
    if request.method == 'POST':
        nombre = request.form['nombre']
        tipo_lector = request.form['tipo_lector']
        add_persona(driver, id, nombre, tipo_lector) 
        return "Persona añadida con éxito."
    personas = get_persona(driver, 4) 
    return render_template('personas.html', personas=personas)

if __name__ == '__main__':
    app.run(debug=True)
