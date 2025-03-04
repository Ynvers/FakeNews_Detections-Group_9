import os
import joblib
import requests
from dotenv import load_dotenv
from mistralai import Mistral
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, Form, UploadFile

load_dotenv()
mistral_key = os.getenv("MISTRAL_KEY")
model = None # Charger le modèle ici
#model = joblib.load("model.pkl")

app = FastAPI()

@app.post("/analyze")
async def predict(content: str = Form(None), type: str = Form(None), file: UploadFile = File(None)):
    if type == "text":
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        result = analyse_text(content)

    elif type == "url":
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        result = analyse_url(content)

    elif type == "file":
        if not file:
            raise HTTPException(status_code=400, detail="File is required")
        result = analyse_file(file)
    
    else:
        raise HTTPException(status_code=400, detail="Type is required")

    return JSONResponse(content=result)


def analyse_text(content: str):
    prediction = model.predict([content])
    credibility_score = prediction[0]
    return {"credibilityScore": 0.5, "verdict": "fake"}

def analyse_url(content: str):
    response = requests.get(content)
    if response.status_code == 200:
        print("Successfully fetched the webpage!")
        soup = BeautifulSoup(response.content, 'html.parser')
        system = """
        Vous êtes un agent spécialisé dans l'extraction de contenu web. Votre mission est la suivante :

        1. Analyse et parsing : 
            - Identifiez le titre de l'article à partir d'une analyse de la page parser.
            - Localisez le corps de l'article.

        2. Nettoyage du texte :
            - Supprimez les balises HTML et les éléments non pertinents.
            - Formatez le texte de manière à obtenir un contenu clair et lisible.

        3. Sortie structurée :
            - Retournez une chaine de caractère représentant l'article.

        4. Gestion des erreurs :
            - Si la page n’est pas accessible ou si la structure HTML ne correspond pas aux attentes, renvoyez un message d’erreur explicite.

        Votre réponse finale doit fournir le titre et le corps de l'article dans un format clair et structuré.  
        """

        context = [
            {
                "role": "system", 
                "content": system
            },
            {
                "role" : "user",
                "content": str(soup)
            }
        ]
        agent = Mistral(mistral_key)
        model_response = agent.chat.complete(
                model = "mistral-large-latest",
                messages = context
        )
        response_message = model_response.choices[0].message.content
        prediction = model.predict([response_message])
        credibility_score = prediction[0]
        verdict = "fake" if credibility_score < 0.5 else "real"
        return {"credibilityScore": credibility_score, "verdict": verdict}
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return {"credibilityScore": 0.5, "verdict": "fake"}

async def analyse_file(file: UploadFile):
    file_content = await file.read()
    prediction = model.predict([file_content.decode('utf-8')])
    return {"credibilityScore": 0.5, "verdict": "fake"}