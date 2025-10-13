def get_persona(driver, pId):
    result = driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}) "
        "RETURN p",
        idPersona = int(pId))
    if result.records == []:
        return None
    return result.records[0].data()["p"]

def update_persona(driver, pId, pNombre, pTipoLector):
    query = """
    MATCH (p:Persona {id: $idPersona})
    SET p.Nombre = $Nombre, p.TipoLector = $TipoLector
    """
    params = {
        "idPersona": int(pId),
        "Nombre": pNombre,
        "TipoLector": pTipoLector
    }
    driver.execute_query(query, params)
    
def add_persona(driver, pId, pNombre, pTipoLector):
    query = (
        "CREATE (p:Persona {id: $id, Nombre: $Nombre, TipoLector: $TipoLector})"
    )
    
    params = {
        "id": int(pId),
        "Nombre": pNombre,
        "TipoLector": pTipoLector
    }
    
    driver.execute_query(query, params)

def add_personas(driver, pListaPersonas):
    for persona in pListaPersonas:
        add_persona(driver, persona["id"], persona["nombre"], persona["tipolector"])
        
def listar_personas(driver):
    query_result = driver.execute_query(
        "MATCH (p:Persona) RETURN p.id AS id, p.Nombre AS nombre, p.TipoLector AS tipoLector ORDER BY p.id"
    )
    
    try:
        records = query_result.records
    except AttributeError:
        records = query_result 

    personas = {}
    
    for record in records:
        try:
            persona_id = record[0] 
            nombre = record[1]
            tipo_lector = record[2]
            
        except (TypeError, IndexError):
            persona_id = record['id'] 
            nombre = record['nombre']
            tipo_lector = record['tipoLector']
        
        personas[persona_id] = {
            "nombre": nombre,
            "tipo_lector": tipo_lector
        }
    
    return personas

def generar_id_persona(driver):

    result = listar_personas(driver) 
    total_personas = len(result) 
    nuevo_id = total_personas + 1

    return str(nuevo_id)