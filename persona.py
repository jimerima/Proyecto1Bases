def get_persona(driver, pId):
    result = driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}) "
        "RETURN p",
        idPersona = int(pId))
    if result.records == []:
        return None
    return result.records[0].data()["p"]


def update_persona(driver, pId, pNombre, pTipoLector):
    if get_persona(driver, pId) is None:
        print(f"No se puede actualizar. No se encontró la persona con id {pId}.")
        return
    driver.execute_query(
        "MATCH (p:Persona {id: $idPersona}) "
        "SET p.Nombre = $Nombre, p.TipoLector = $TipoLector",
        idPersona = int(pId), Nombre = pNombre, TipoLector = pTipoLector
    )
    

def add_persona(driver, pId, pNombre, pTipoLector):
    driver.execute_query(
        "MERGE (p:Persona {id: $idPersona, Nombre: $Nombre, TipoLector: $TipoLector})",
        idPersona = int(pId), Nombre = pNombre, TipoLector = pTipoLector
    )

def add_personas(driver, pListaPersonas):
    for persona in pListaPersonas:
        add_persona(driver, persona["id"], persona["Nombre"], persona["TipoLector"])
        print("Persona añadida:", persona["Nombre"])

def listar_personas(driver):
    result = driver.execute_query(
        "MATCH (p:Persona) RETURN p.idPersona AS id, p.Nombre AS nombre, p.TipoLector AS tipoLector"
    )

    personas = {}
    for record in result:
        personas[record['id']] = {
            "nombre": record['nombre'],
            "tipo_lector": record['tipoLector']
        }
    
    return personas


def generar_id_persona(driver):
    result = driver.execute_query("MATCH (p:Persona) RETURN count(p) AS total")
    total_personas = result[0]['total']
    
    nuevo_id = total_personas + 1
    return nuevo_id