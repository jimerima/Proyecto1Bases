def add_autoria(driver, pIdAutor, pIdLibro):
    driver.execute_query(
        "MATCH (a:Autor {idAutor: $idAutor}), (l:Libro {idLibro: $idLibro}) "
        "MERGE (a)-[:ESCRIBIO]->(l)",
        idAutor = int(pIdAutor), idLibro = int(pIdLibro)
    )

def add_autorias(driver, pListaAutorias):
    for autoria in pListaAutorias:
        add_autoria(driver, autoria["idAutor"], autoria["idLibro"])
        print("Autoría añadida:", autoria["idAutor"], "-", autoria["idLibro"])