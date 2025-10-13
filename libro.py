def get_libro(driver, pIdLibro):
    result = driver.execute_query(
        "MATCH (l:Libro {idLibro: $idLibro}) "
        "RETURN l",
        idLibro = int(pIdLibro)) 
    if result.records == []:
        return None
    return result.records[0].data()["l"]

def update_libro(driver, pIdLibro, pTitulo, pGenero, pAnno):
    query = """
    MATCH (l:Libro {idLibro: $idLibro})
    SET l.Titulo = $Titulo, 
        l.Genero = $Genero, 
        l.Anno = $Anno
    """
    params = {
        "idLibro": int(pIdLibro),
        "Titulo": pTitulo,
        "Genero": pGenero,
        "Anno": int(pAnno)
    }
    driver.execute_query(query, params)

def add_libro(driver, pIdLibro, pTitulo, pGenero, pAnno):
    query = (
        "CREATE (l:Libro {idLibro: $idLibro, Titulo: $Titulo, Genero: $Genero, Anno: $Anno})"
    )
    
    params = {
        "idLibro": int(pIdLibro),
        "Titulo": pTitulo,
        "Genero": pGenero,
        "Anno": int(pAnno) 
    }
    
    driver.execute_query(query, params)

def add_libros(driver, pListaLibros):
    for libro in pListaLibros:
        add_libro(driver, libro["idlibro"], libro["titulo"], libro["genero"], libro["anno"])
        
def listar_libros(driver):
    query_result = driver.execute_query(
        "MATCH (l:Libro) RETURN l.idLibro AS idLibro, l.Titulo AS titulo, l.Genero AS genero, l.Anno AS anno ORDER BY l.idLibro"
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
    return libros

def generar_id_libro(driver):
    query_result = driver.execute_query(
        "MATCH (l:Libro) RETURN l.idLibro AS idLibro ORDER BY l.idLibro DESC LIMIT 1"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 
        
    ultimo_id = 0

    try:
        ultimo_id = records[0][0] 
        nuevo_id = ultimo_id + 1
        
    except (IndexError, TypeError):
        nuevo_id = 1 
    
    return str(nuevo_id)
