def get_libro(driver, pIdLibro):
    result = driver.execute_query(
        "MATCH (l:Libro {idLibro: $idLibro}) "
        "RETURN l",
        idLibro = int(pIdLibro)) 
    if result.records == []:
        return None
    return result.records[0].data()["l"]

def update_libro(driver, pIdLibro, pTitulo, pGenero, pAnno):
    if get_libro(driver, pIdLibro) is None:
        print(f"No se puede actualizar. No se encontró el libro con id {pIdLibro}.")
        return
    driver.execute_query(
        "MATCH (l:Libro {idLibro: $idLibro}) "
        "SET l.Titulo = $Titulo, l.Genero = $Genero, l.Anno = $Anno",
        idLibro = int(pIdLibro), Titulo = pTitulo, Genero = pGenero, Anno = pAnno
    )

def add_libro(driver, pIdLibro, pTitulo, pGenero, pAnno):
    driver.execute_query(
        "MERGE (l:Libro {idLibro: $idLibro, Titulo: $Titulo, Genero: $Genero, Anno: $Anno})",
        idLibro = int(pIdLibro), Titulo = pTitulo, Genero = pGenero, Anno = pAnno
    )

def add_libros(driver, pListaLibros):
    for libro in pListaLibros:
        add_libro(driver, libro["idLibro"], libro["Titulo"], libro["Genero"], libro["Anno"])
        print("Libro añadido:", libro["Titulo"])