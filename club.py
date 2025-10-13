def get_club(driver, pIdClub):
    result = driver.execute_query(
        "MATCH (c:Club {idClub: $idClub}) "
        "RETURN c",
        idClub = int(pIdClub)) 
    if result.records == []:
        return None
    return result.records[0].data()["c"]

def update_club(driver, pIdClub, pNombre, pUbicacion, pTematica):
    query = """
    MATCH (c:Club {idClub: $idClub})
    SET c.Nombre = $Nombre, c.Ubicacion = $Ubicacion, c.Tematica = $Tematica
    """
    params = {
        "idClub": int(pIdClub),
        "Nombre": pNombre,
        "Ubicacion": pUbicacion,
        "Tematica": pTematica
    }
    driver.execute_query(query, params)

def add_club(driver, pIdClub, pNombre, pUbicacion, pTematica):
    query = (
        "CREATE (c:Club {idClub: $idClub, Nombre: $Nombre, Ubicacion: $Ubicacion, Tematica: $Tematica})"
    )
    
    params = {
        "idClub": int(pIdClub),
        "Nombre": pNombre,
        "Ubicacion": pUbicacion,
        "Tematica": pTematica
    }
    
    driver.execute_query(query, params)

def add_clubs(driver, pListaClubs):
    for club in pListaClubs:
        add_club(driver, club["idclub"], club["nombre"], club["ubicacion"], club["tematica"])
        
def listar_clubs(driver):
    query_result = driver.execute_query(
        "MATCH (c:Club) RETURN c.idClub AS idClub, c.Nombre AS nombre, c.Ubicacion AS ubicacion, c.Tematica AS tematica ORDER BY c.idClub"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 

    clubs = {}
    
    for record in records:
        try:
            club_id = record[0] 
            nombre = record[1]
            ubicacion = record[2]
            tematica = record[3]
            clubs[club_id] = {
                "idClub": club_id,
                "nombre": nombre,
                "ubicacion": ubicacion,
                "tematica": tematica 
            }
        except (KeyError, IndexError) as e:
            club_str = str(club_id) if 'club_id' in locals() else 'N/A'
            print(f"Error al procesar el registro con ID {club_str}: {e}")
            
    return clubs

def generar_id_club(driver):
    query_result = driver.execute_query(
        "MATCH (c:Club) RETURN c.idClub AS idClub ORDER BY c.idClub DESC LIMIT 1"
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