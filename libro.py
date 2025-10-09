def get_libro(driver, pIdLibro):
    result = driver.execute_query(
        "MATCH (l:Libro {idLibro: $idLibro}) "
        "RETURN l",
        idLibro = int(pIdLibro)) 
    if result.records == []:
        return None
    return result.records[0].data()["l"]

def update_libro(driver, lId, lTitulo, lGenero, lAnno):
    lId_int = int(lId)
    lAnno_int = int(lAnno)

    query = """
    MATCH (l:Libro {idLibro: $idLibro})
    SET l.Titulo = $Titulo,
        l.Genero = $Genero,
        l.Anno = $Anno
    """
    params = {
        "idLibro": lId_int,
        "Titulo": lTitulo,
        "Genero": lGenero,
        "Anno": lAnno_int
    }
    driver.execute_query(query, params)

def add_libro(driver, lId, lTitulo, lGenero, lAnno):
    try:
        lId_int = int(lId)
        lAnno_int = int(lAnno)
    except ValueError as e:
        print(f"Error de conversión de tipo: {e}")
        return

    query = """
    CREATE (l:Libro {
        idLibro: $idLibro, 
        Titulo: $Titulo, 
        Genero: $Genero, 
        Anno: $Anno
    })
    """
    
    params = {
        "idLibro": lId_int,
        "Titulo": lTitulo,
        "Genero": lGenero,
        "Anno": lAnno_int 
    }
    
    driver.execute_query(query, params)
    
    print(f"Libro {lTitulo} creado con ID: {lId}")
    
    driver.execute_query(query, params)

def add_libros(driver, pListaLibros):
    for libro in pListaLibros:
        add_libro(driver, libro["idLibro"], libro["Titulo"], libro["Genero"], libro["Anno"])
        print("Libro añadido:", libro["Titulo"])

def listar_libros(driver):
    query_result = driver.execute_query(
        "MATCH (l:Libro) RETURN l.idLibro AS idLibro, l.Titulo AS titulo, l.Genero AS genero, l.Anno AS anno"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 

    libros = {}
    
    for record in records:
        try:
            libro_id = record[0] 
            titulo = record[1]
            genero = record[2]
            anno = record[3]
            
            libros[libro_id] = {
                "idLibro": libro_id,
                "titulo": titulo,        
                "genero": genero,
                "anno": anno
            }
        except (KeyError, IndexError) as e:
            libro_str = str(libro_id) if 'libro_id' in locals() else 'N/A'
            print(f"Error al procesar el registro con ID {libro_str}: {e}")

def generar_id_libro(driver):
    query_result = driver.execute_query(
        "MATCH (l:Libro) RETURN MAX(l.idLibro) AS max_id"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 

    max_id = 0
    for record in records:
        try:
            max_id = record["max_id"] if record["max_id"] is not None else 0
        except KeyError as e:
            print(f"Error al obtener el ID máximo del libro: {e}")
    
    return str(max_id + 1)
