def get_miembros(driver, pIdClub): 
    resultado = driver.execute_query(
        "MATCH (p:Persona)-[:PERTENECE_A]->(c:Club {idClub: $idClub}) "
        "RETURN p.id AS id, p.Nombre AS Nombre ORDER BY p.id",
        idClub = int(pIdClub)
    )

    records = resultado.records

    miembros = []
    for record in records:
        try:
            miembros.append({"id":record[0],"Nombre":record[1]})
        except (KeyError, IndexError) as e:
            print(f"Error procesando el registro {record}: {e}")
    return miembros

def add_membresia(driver, pIdPersona, pIdClub):
    query = "MATCH (p:Persona {id: $idPersona}), (c:Club {idClub: $idClub}) MERGE (p)-[:PERTENECE_A]->(c)"

    params = {
        "idPersona": int(pIdPersona),
        "idClub": int(pIdClub)
    }

    driver.execute_query(query, params)

def add_membresias(driver, pListaMembresias):
    for membresia in pListaMembresias:
        add_membresia(driver, membresia["id"], membresia["idClub"])
        #print("Membresía añadida:", membresia["id"])