def get_lecturas(driver, pIdPersona):
    resultado = driver.execute_query(
        "MATCH (p:Persona {id: $idPersona})-[:LEE]->(l:Libro) "
        "RETURN l.idLibro AS idLibro, l.Titulo AS Titulo, l.Genero AS Genero, l.Anno AS anno ORDER BY l.idLibro",
        idPersona = int(pIdPersona)
    )
    
    records = resultado.records
    
    libros_leidos = []
    for record in records:
        try:
            libros_leidos.append({"idLibro":record[0], "Titulo":record[1], "Genero":record[2], "Anno":record[3]})
        except (KeyError, IndexError) as e:
            print(f"Error procesando el registro {record}: {e}")
            
    return libros_leidos

def add_lectura(driver, pIdPersona, pIdLibro):
    driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}), (l:Libro {idLibro: $idLibro}) "
        "MERGE (p)-[:LEE]->(l)",
        idPersona = int(pIdPersona), idLibro = int(pIdLibro)
    )

def add_lecturas(driver, pListaLecturas):
    for lectura in pListaLecturas:
        add_lectura(driver, lectura["id"], lectura["idlibro"])
        