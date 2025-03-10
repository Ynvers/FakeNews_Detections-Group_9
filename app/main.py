import os
import re
import fitz
import joblib
import string
import numpy as np
import requests
from dotenv import load_dotenv
from mistralai import Mistral
from bs4 import BeautifulSoup
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()
mistral_key = os.getenv("MISTRAL_API_KEY")
model = joblib.load("model/model.pkl")
vectorizer = joblib.load("model/tfidf_vectorizer.pkl")
print(f"Type de model : {type(model)}")  # Doit être un modèle ML, pas un Vectorizer
print(f"Type de vectorizer : {type(vectorizer)}")  # Doit être un TfidfVectorizer


app = FastAPI()

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Autorise toutes les origines (pour le développement)
    allow_credentials=True,
    allow_methods=["*"],  # Autorise toutes les méthodes (GET, POST, etc.)
    allow_headers=["*"],  # Autorise tous les headers
)

@app.post("/analyze")
async def predict(content: str = Form(None), type: str = Form(None), file: UploadFile = File(None)):
    #print(f"l'entrée {file}")
    if type == "text":
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        result = await analyse_text(content)

    elif type == "url":
        if not content:
            raise HTTPException(status_code=400, detail="Content is required")
        result = await analyse_url(content)

    elif file.content_type == "application/pdf":
        print(f"Received file: {file.filename}")
        if not file:
            raise HTTPException(status_code=400, detail="File is required")
        result = await analyse_file(file)
    
    else:
        raise HTTPException(status_code=400, detail="Type is required")

    return JSONResponse(content=result)


async def analyse_text(content: str):
    #prediction = model.predict([content])
    #credibility_score = prediction[0]
    return predict_text(content)

async def analyse_url(content: str):
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

      Votre réponse finale doit fournir le corps de l'article dans un format clair et structuré comme un article de presse sans le format markedown, juste une chaine de carcatère.
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
                model = "codestral-latest",
                messages = context
        )
        response_message = model_response.choices[0].message.content
        # prediction = model.predict([response_message])
        # credibility_score = prediction[0]
        # verdict = "fake" if credibility_score < 0.5 else "real"
        return predict_text(response_message)
    else:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")

async def analyse_file(file: UploadFile):
    file_content = await file.read()

    # Extraire le texte du PDF
    with fitz.open(stream=file_content, filetype="pdf") as doc:
        text = "\n".join([page.get_text() for page in doc])

    return predict_text(text)

def predict_text(text: str):
    # Nettoyer le texte
    text = wordopt(text)
    # Transformer le texte en vecteur
    vectorized_text = vectorizer.transform([text])
    # Prédiction avec le modèle xgboost
    credibility_score = model.predict_proba(vectorized_text)
    probas_score = (round((float(credibility_score[0][1])*100), 3) ) * 100
    print(f"Probas score: {probas_score}")
    verdict = "Fake News" if probas_score < 50 else "Real News"
    return {
        "credibilityScore": probas_score,
        "verdict": verdict,
    }

def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text