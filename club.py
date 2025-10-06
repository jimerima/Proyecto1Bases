def get_club(driver, pIdClub):
    result = driver.execute_query(
        "MATCH (c:Club {idClub: $idClub}) "
        "RETURN c",
        idClub = int(pIdClub)) 
    if result.records == []:
        return None
    return result.records[0].data()["c"]

def update_club(driver, pIdClub, pUbicacion, pTematica):
    if get_club(driver, pIdClub) is None:
        print(f"No se puede actualizar. No se encontró el club con id {pIdClub}.")
        return
    driver.execute_query(
        "MATCH (c:Club {idClub: $idClub}) "
        "SET c.Ubicacion = $Ubicacion, c.Tematica = $Tematica",
        idClub = int(pIdClub), Ubicacion = pUbicacion, Tematica = pTematica
    )

def add_club(driver, pIdClub, pUbicacion, pTematica):
    driver.execute_query(
        "MERGE (c:Club {idClub: $idClub, Ubicacion: $Ubicacion, Tematica: $Tematica})",
        idClub = int(pIdClub), Ubicacion = pUbicacion, Tematica = pTematica
    )

def add_clubs(driver, pListaClubs):
    for club in pListaClubs:
        add_club(driver, club["idClub"], club["Ubicacion"], club["Tematica"])
        print("Club añadido:", club["Ubicacion"])