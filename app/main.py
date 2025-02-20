import re
import joblib
from fastapi import FASTAPI, HTTPException


app = FASTAPI()

model = None # Charger le modèle ici

class Article:
    title: str
    content: str

@app.post("/predict")
async def predict(article: Article):
    result = "Fake"
    return {"result": result}