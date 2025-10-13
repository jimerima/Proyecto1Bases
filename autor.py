def get_autor(driver, pIdAutor):
    result = driver.execute_query(
        "MATCH (a:Autor {idAutor: $idAutor}) "
        "RETURN a",
        idAutor = int(pIdAutor)) 
    if result.records == []:
        return None
    return result.records[0].data()["a"]

def update_autor(driver, pIdAutor, pNombre, pNacionalidad):
    query = """
    MATCH (a:Autor {idAutor: $idAutor})
    SET a.Nombre = $Nombre, a.Nacionalidad = $Nacionalidad
    """
    params = {
        "idAutor": int(pIdAutor),
        "Nombre": pNombre,
        "Nacionalidad": pNacionalidad
    }
    driver.execute_query(query, params)

def add_autor(driver, pIdAutor, pNombre, pNacionalidad):
    query = (
        "CREATE (a:Autor {idAutor: $idAutor, Nombre: $Nombre, Nacionalidad: $Nacionalidad})"
    )
    
    params = {
        "idAutor": int(pIdAutor),
        "Nombre": pNombre,
        "Nacionalidad": pNacionalidad
    }
    
    driver.execute_query(query, params)

def add_autores(driver, pListaAutores):
    for autor in pListaAutores:
        add_autor(driver, autor["idautor"], autor["nombre"], autor["nacionalidad"])

def listar_autores(driver):
    query_result = driver.execute_query(
    "MATCH (a:Autor) RETURN a.idAutor AS idAutor, a.Nombre AS nombre, a.Nacionalidad AS nacionalidad ORDER BY a.idAutor"
    )   
    
    #try:
    records = query_result.records
    #except AttributeError:
        #records = query_result 

    autores = {}
    
    for record in records:
        try:
            autor_id = record[0] 
            nombre = record[1]
            nacionalidad = record[2]
            
            autores[autor_id] = {
                "idAutor": autor_id,
                "nombre": nombre,        
                "nacionalidad": nacionalidad 
            }
        except (KeyError, IndexError) as e:
            autor_str = str(autor_id) if 'autor_id' in locals() else 'N/A'
            print(f"Error al procesar el registro con ID {autor_str}: {e}")
    return autores

def generar_id_autor(driver):
    query_result = driver.execute_query(
        "MATCH (a:Autor) RETURN a.idAutor AS idAutor ORDER BY a.idAutor DESC LIMIT 1"
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