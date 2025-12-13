from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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
import numpy as np

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

@app.post("/analyze")
async def analyze(
	file: UploadFile = File(None),
	content: str = Form(None),
	type: str = Form(...)
):
	if not model or not vectorizer:
		raise HTTPException(status_code=500, detail="Model not loaded")

	text_to_analyze = ""

	try:
		if type == 'text':
			if not content:
				raise HTTPException(status_code=400, detail="No content provided")
			text_to_analyze = content

		elif type == 'url':
			if not content:
				raise HTTPException(status_code=400, detail="No URL provided")
			response = requests.get(content)
			response.raise_for_status()
			soup = BeautifulSoup(response.text, 'html.parser')
			text_to_analyze = ' '.join([p.text for p in soup.find_all('p')])
			if not text_to_analyze:
				raise HTTPException(status_code=400, detail="No text found at URL")

		elif type == 'file':
			if not file:
				raise HTTPException(status_code=400, detail="No file provided")
			
			# Save temp file
			file_location = f"temp_{file.filename}"
			with open(file_location, "wb") as buffer:
				shutil.copyfileobj(file.file, buffer)
			
			# Read PDF
			doc = fitz.open(file_location)
			for page in doc:
				text_to_analyze += page.get_text()
			doc.close()
			os.remove(file_location)

			if not text_to_analyze:
				raise HTTPException(status_code=400, detail="Could not extract text from PDF")

		else:
			raise HTTPException(status_code=400, detail="Invalid type")

		# Prediction
		clean_text = wordopt(text_to_analyze)
		vec_text = vectorizer.transform([clean_text])
		prediction = model.predict(vec_text)[0]
		
		# Try to get probability for "True News" (Class 1)
		credibility_score = 0
		if hasattr(model, "predict_proba"):
			probs = model.predict_proba(vec_text)
			credibility_score = int(probs[0][1] * 100) # Probability of class 1
		else:
			# Fallback if no proba
			credibility_score = 100 if prediction == 1 else 0

		result = output_label(prediction)

		return {
			"verdict": result,
			"credibilityScore": credibility_score,
			"prediction_class": int(prediction)
		}

	except Exception as e:
		print(f"Error during analysis: {e}")
		raise HTTPException(status_code=500, detail=str(e))

