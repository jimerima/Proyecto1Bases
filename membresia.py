def get_miembros(driver, pIdClub): #para consulta
    result = driver.execute_query(
        "MATCH (p:Persona) WHERE (p)-[PERTENECE_A]->(:Club {idClub: $idClub}) RETURN p.nombre",
        idClub = int(pIdClub))
    if result.records == []:
        return None
    return result.records[0].data()["p"] #gotta double check

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