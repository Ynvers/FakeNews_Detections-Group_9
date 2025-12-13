from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import joblib
import re
import string
import shutil
import os
import requests
from bs4 import BeautifulSoup
import fitz  # PyMuPDF
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Fake News Detection API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Load Models ---
# Assuming run from project root
MODEL_PATH = "app/model/model.pkl"
VECTORIZER_PATH = "app/model/tfidf_vectorizer.pkl"

try:
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("Models loaded successfully.")
except Exception as e:
    print(f"Error loading models: {e}")
    model = None
    vectorizer = None

# --- Preprocessing Function (Must match training) ---
def wordopt(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)
    text = re.sub(r"\\W", " ", text)
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    text = re.sub(r'<.*?>+', '', text)
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub(r'\n', '', text)
    text = re.sub(r'\w*\d\w*', '', text)
    return text

def output_label(n):
    if n == 0:
        return "Fake News"
    elif n == 1:
        return "True News"
    return "Error"

# --- Pydantic Models ---
class TextRequest(BaseModel):
    text: str

class UrlRequest(BaseModel):
    url: str

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "Fake News Detection API is running"}

@app.post("/predict")
def predict_text(request: TextRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    clean_text = wordopt(request.text)
    vec_text = vectorizer.transform([clean_text])
    prediction = model.predict(vec_text)
    
    result = output_label(prediction[0])
    # Assuming Decision Tree, we might not get probabilities easily with standard pickle of just the class predictions if not configured,
    # but let's try to infer simple output first. 
    # If the user used DecisionTreeClassifier, .predict returns class. 
    
    return {"prediction": result, "class_id": int(prediction[0])}

@app.post("/predict-url")
def predict_url(request: UrlRequest):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")

    try:
        response = requests.get(request.url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        # Simple extraction: all paragraph text
        text = ' '.join([p.text for p in soup.find_all('p')])
        
        if not text:
            raise HTTPException(status_code=400, detail="No text found at URL")

        clean_text = wordopt(text)
        vec_text = vectorizer.transform([clean_text])
        prediction = model.predict(vec_text)
        result = output_label(prediction[0])
        
        return {"prediction": result, "class_id": int(prediction[0]), "excerpt": text[:200] + "..."}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/predict-pdf")
async def predict_pdf(file: UploadFile = File(...)):
    if not model or not vectorizer:
        raise HTTPException(status_code=500, detail="Model not loaded")
        
    try:
        # Save temp file
        file_location = f"temp_{file.filename}"
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Read PDF
        doc = fitz.open(file_location)
        text = ""
        for page in doc:
            text += page.get_text()
            
        doc.close()
        os.remove(file_location) # Clean up

        if not text:
            raise HTTPException(status_code=400, detail="Could not extract text from PDF")

        clean_text = wordopt(text)
        vec_text = vectorizer.transform([clean_text])
        prediction = model.predict(vec_text)
        result = output_label(prediction[0])
        
        return {"prediction": result, "class_id": int(prediction[0]), "excerpt": text[:200] + "..."}

    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail=str(e))
