def get_mas_libros_leidos(driver):
    query = """MATCH (p:Persona)-[:PERTENECE_A]->(c:Club)
                MATCH (p)-[:LEE]->(l:Libro)<-[:RECOMIENDA]-(c)
                WITH p, c, count(DISTINCT l) AS cantidad
                WHERE cantidad >= 3
                RETURN coalesce(p.Nombre) AS Persona,
                    coalesce(c.Nombre) AS Club,
                    cantidad AS LibrosRecomendadosLeidos
                ORDER BY LibrosRecomendadosLeidos DESC, Persona ASC, Club ASC;"""
    
    resultado = driver.execute_query(query)
    records = resultado.records
    resultados = []
    for record in records:
        resultados.append({
            "Persona": record.get("Persona"),
            "Club": record.get("Club"),
            "LibrosRecomendadosLeidos": record.get("LibrosRecomendadosLeidos")
        })
    return resultados

def get_personas_en_mas_clubes(driver):
    query = """MATCH (p:Persona)-[:PERTENECE_A]->(c:Club)
               WITH p, collect(coalesce(c.Nombre)) AS Clubes
               RETURN coalesce(p.Nombre) AS Persona, Clubes
               ORDER BY size(Clubes) DESC, Persona ASC;"""

    resultado = driver.execute_query(query)
    records = resultado.records
    resultados = []

    for record in records:
        resultados.append({
            "Persona": record.get("Persona"),
            "Clubes": record.get("Clubes")
        })
    return resultados