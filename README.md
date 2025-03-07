# 📰 Fake News Detection - TP de Classe

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?style=for-the-badge&logo=fastapi)
![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 📌 Description
Ce projet est un travail pratique (TP) réalisé dans un cadre académique. Il vise à concevoir et implémenter une application web permettant de détecter les fake news à l'aide de modèles de Machine Learning et de techniques de traitement du langage naturel (NLP).

## ✨ Fonctionnalités
- ✅ Analyse de texte pour identifier les fake news.
- 🔍 Vérification d'articles via une URL.
- 📄 Extraction et analyse de texte depuis des documents PDF.
- 🌐 Interface web interactive pour faciliter l'utilisation.

## 🛠️ Technologies Utilisées
- **Backend** : FastAPI
- **Frontend** : HTML, CSS, JavaScript
- **Machine Learning** : XGBoost, Scikit-learn, TfidfVectorizer
- **Autres** : BeautifulSoup (scraping), PyMuPDF (extraction de texte depuis un PDF)

## 🚀 Installation et Exécution
### 📌 Prérequis
- Python 3.8+
- pip
- Virtualenv (optionnel)

### 💞 Installation
1. **Cloner le projet**
   ```bash
   git clone https://github.com/Ynvers/FakeNews_Detections-Group_9.git
   cd FakeNews_Detections-Group_9
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python -m venv env
   source env/bin/activate  # Sur macOS/Linux
   env\Scripts\activate    # Sur Windows
   ```

3. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application**
   ```bash
   cd app
   uvicorn main:app --reload
   ```

## 🎯 Utilisation
Une fois l'application lancée, ouvrez votre navigateur et accédez à l'interface via **index.html** dans le dossier `Front_end/`.

## 📂 Organisation du Projet
```
├── app/
│   ├── model/
│   │   ├── model.pkl             # Modèle de classification
│   │   ├── tfidf_vectorizer.pkl  # Vectoriseur TF-IDF
│   │
│   ├── main.py                   # API avec FastAPI
│
├── Front_end/
│   ├── history.html               # Historique des prédictions
│   ├── history.js                 # Gestion de l'historique
│   ├── index.html                 # Interface principale
│   ├── script.js                  # Script principal
│   ├── styles.css                 # Feuille de style
│
├── venv/                          # Environnement virtuel (optionnel)
├── .env                           # Variables d'environnement
├── .gitignore                     # Fichiers ignorés par Git
├── README.md                      # Documentation du projet
├── requirements.txt                # Dépendances
```

## 📌 Exemples d'Utilisation
![Demo](image.png)  
*(Illustration du fonctionnement du projet.)*

## 🔮 Améliorations Futures
- 📈 Intégration de modèles avancés (BERT, RoBERTa, etc.)
- 🎨 Amélioration de l'interface utilisateur
- 🗄 Ajout d'une base de données pour conserver les analyses

## 👥 Auteurs
- **Nathan** - [GitHub](https://github.com/Ynvers) | [LinkedIn](https://www.linkedin.com/in/ton-profil)
- **Coéquipier 1** - [GitHub](https://github.com/coequipier1) | [LinkedIn](https://www.linkedin.com/in/coequipier1)
- **Coéquipier 2** - [GitHub](https://github.com/coequipier2) | [LinkedIn](https://www.linkedin.com/in/coequipier2)

## 🐝 Licence
Ce projet est sous licence MIT. Vous pouvez l'utiliser et le modifier librement.

## 🤝 Contribuer
Les contributions sont les bienvenues !
1. **Fork** le projet 📌
2. **Crée une branche** (`git checkout -b feature-nouvelle-fonctionnalité`)
3. **Commit tes modifications** (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. **Push** sur la branche (`git push origin feature-nouvelle-fonctionnalité`)
5. **Crée une Pull Request** 🎉

