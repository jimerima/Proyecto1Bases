def add_recomendacion(driver, pIdClub, pIdLibro):
    driver.execute_query(
        "MATCH (c:Club {idClub: $idClub}), (l:Libro {idLibro: $idLibro}) "
        "MERGE (c)-[:RECOMIENDA]->(l)",
        idClub = int(pIdClub), idLibro = int(pIdLibro)
    )

def add_recomendaciones(driver, pListaRecomendaciones):
    for recomendacion in pListaRecomendaciones:
        add_recomendacion(driver, recomendacion["idClub"], recomendacion["idLibro"])
        print("Recomendación añadida:", recomendacion["idClub"], "-", recomendacion["idLibro"])
