def get_autor(driver, pIdAutor):
    result = driver.execute_query(
        "MATCH (a:Autor {idAutor: $idAutor}) "
        "RETURN a",
        idAutor = int(pIdAutor)) 
    if result.records == []:
        return None
    return result.records[0].data()["a"]

def update_autor(driver, pIdAutor, pNombre, pNacionalidad):
    if get_autor(driver, pIdAutor) is None:
        print(f"No se puede actualizar. No se encontró el autor con id {pIdAutor}.")
        return
    driver.execute_query(
        "MATCH (a:Autor {idAutor: $idAutor}) "
        "SET a.Nombre = $Nombre, a.Nacionalidad = $Nacionalidad",
        idAutor = int(pIdAutor), Nombre = pNombre, Nacionalidad = pNacionalidad
    )

def add_autor(driver, pIdAutor, pNombre, pNacionalidad):
    driver.execute_query(
        "MERGE (a:Autor {idAutor: $idAutor, Nombre: $Nombre, Nacionalidad: $Nacionalidad})",
        idAutor = int(pIdAutor), Nombre = pNombre, Nacionalidad = pNacionalidad
    )

def add_autores(driver, pListaAutores):
    for autor in pListaAutores:
        add_autor(driver, autor["idAutor"], autor["Nombre"], autor["Nacionalidad"])
        print("Autor añadido:", autor["Nombre"])