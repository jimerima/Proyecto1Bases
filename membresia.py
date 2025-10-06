def add_membresia(driver, pIdPersona, pIdClub):
    driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}), (c:Club {idClub: $idClub}) "
        "MERGE (p)-[:PERTENECE_A]->(c)",
        idPersona = int(pIdPersona), idClub = int(pIdClub)
    )

def add_membresias(driver, pListaMembresias):
    for membresia in pListaMembresias:
        add_membresia(driver, membresia["id"], membresia["idClub"])
        print("Membresía añadida:", membresia["id"])