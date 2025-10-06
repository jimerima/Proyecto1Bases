def add_lectura(driver, pIdPersona, pIdLibro):
    driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}), (l:Libro {idLibro: $idLibro}) "
        "MERGE (p)-[:LEE]->(l)",
        idPersona = int(pIdPersona), idLibro = int(pIdLibro)
    )

def add_lecturas(driver, pListaLecturas):
    for lectura in pListaLecturas:
        add_lectura(driver, lectura["id"], lectura["idLibro"])
        print("Lectura añadida:", lectura["id"], "-", lectura["idLibro"])