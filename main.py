from fastapi import FastAPI, HTTPException
from neo4j import GraphDatabase

app = FastAPI(title="Movie Recommendation API")

# Neo4j Database Credentials
URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "ADBMS9016"  

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

@app.get("/recommend/{movie_title}")
def get_recommendations(movie_title: str):
    query = """
    MATCH (m:Movie)
    WHERE toLower(m.title) CONTAINS toLower($title)
    MATCH (m)<-[:RATED]-(u:User)-[:RATED]->(rec:Movie)
    WHERE m <> rec
    RETURN rec.title AS recommended_movie, COUNT(rec) AS score
    ORDER BY score DESC LIMIT 5
    """
    
    try:
        with driver.session() as session:
            result = session.run(query, title=movie_title)
            recommendations = [{"title": record["recommended_movie"], "score": record["score"]} for record in result]
            
            if not recommendations:
                # Error message changed to English
                return {"message": f"No recommendations found for '{movie_title}'. Please check the spelling."}
                
            return {"movie": movie_title, "recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))