def get_club(driver, pIdClub):
    result = driver.execute_query(
        "MATCH (c:Club {idClub: $idClub}) "
        "RETURN c",
        idClub = int(pIdClub)) 
    if result.records == []:
        return None
    return result.records[0].data()["c"]

def update_club(driver, pIdClub, pUbicacion, pTematica):
    query = """
    MATCH (c:Club {idClub: $idClub})
    SET c.Ubicacion = $Ubicacion, c.Tematica = $Tematica
    """
    params = {
        "idClub": int(pIdClub),
        "Ubicacion": pUbicacion,
        "Tematica": pTematica
    }
    driver.execute_query(query, params)

def add_club(driver, pIdClub, pUbicacion, pTematica):
    query = (
        "CREATE (c:Club {idClub: $idClub, Ubicacion: $Ubicacion, Tematica: $Tematica})"
    )
    
    params = {
        "idClub": int(pIdClub),
        "Ubicacion": pUbicacion,
        "Tematica": pTematica
    }
    
    driver.execute_query(query, params)

def add_clubs(driver, pListaClubs):
    for club in pListaClubs:
        add_club(driver, club["idClub"], club["Ubicacion"], club["Tematica"])
        print("Club añadido:", club["Ubicacion"])

def listar_clubs(driver):
    query_result = driver.execute_query(
        "MATCH (c:Club) RETURN c.idClub AS idClub, c.Ubicacion AS ubicacion, c.Tematica AS tematica"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 

    clubs = {}
    
    for record in records:
        try:
            club_id = record[0] 
            ubicacion = record[1]
            tematica = record[2]
            
            clubs[club_id] = {
                "idClub": club_id,
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