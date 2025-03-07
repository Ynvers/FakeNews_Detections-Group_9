# 📰 Fake News Detection - TP de Classe

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green?style=for-the-badge&logo=fastapi)
![MIT License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

## 📌 Description
Ce projet est un travail pratique (TP) réalisé dans un cadre académique. Il consiste en la conception et l'implémentation d'un site web permettant la détection de fake news à l'aide de modèles de Machine Learning. L'objectif est d'explorer l'utilisation de techniques de traitement du langage naturel (NLP) pour évaluer la crédibilité d'un texte ou d'un article.

## ✨ Fonctionnalités
- ✅ Analyse de texte pour déterminer s'il s'agit d'une fake news.
- 🔍 Analyse d'articles à partir d'une URL.
- 📄 Analyse de documents PDF.
- 🌐 Interface web interactive permettant aux utilisateurs d'effectuer des prédictions.

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

### 📥 Installation
1. **Cloner le projet**
   ```bash
   git clone https://github.com/Ynvers/FakeNews_Detections-Group_9.git
   cd FakeNews_Detections-Group_9
   ```

2. **Créer un environnement virtuel (optionnel mais recommandé)**
   ```bash
   python -m venv env
   source venv/bin/activate  # Sur macOS/Linux
   venv\Scripts\activate     # Sur Windows
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
Une fois l'application lancée, ouvrez votre navigateur et accédez à la page **index.html** dans le dossier `Front_end/`.

## 📂 Organisation du Projet
```
├── app/
│   ├── model/
│   │   ├── model.pkl             # Modèle de classification
│   │   ├── tfidf_vectorizer.pkl  # Vectoriseur TF-IDF
│   │
│   ├── main.py                   # Code principal (API avec FastAPI)
│
├── Front_end/
│   ├── history.html               # Page historique des prédictions
│   ├── history.js                 # Script pour la gestion de l'historique
│   ├── index.html                 # Page principale de l'application
│   ├── script.js                  # Script principal du frontend
│   ├── styles.css                 # Feuille de style CSS
│
├── venv/                          # Environnement virtuel (optionnel)
├── .env                           # Variables d'environnement
├── .gitignore                     # Fichiers ignorés par Git
├── README.md                      # Documentation du projet
├── requirements.txt                # Liste des dépendances
```

## 🔮 Améliorations Futures
- 📈 Intégration d'un modèle plus performant (BERT, RoBERTa, etc.)
- 🎨 Optimisation de l'interface utilisateur
- 🗄️ Ajout d'une base de données pour stocker les résultats des analyses

## 👥 Auteurs
- **Nathan ADOHO** - [GitHub](https://github.com/Ynvers) | [LinkedIn](www.linkedin.com/in/luzoloadoho)
- **Abiola SALAMI** - [GitHub](https://github.com/abiolasalami) | [LinkedIn](https://www.linkedin.com/in/abiola-salami-ab2b15300 )
- **Farid MAMADOU** - [GitHub](https://github.com/faridmamadou) | [LinkedIn](https://www.linkedin.com/in/coequipier2)
- **Nelly DAKO** - [GitHub](https://github.com/Beretta05) | [LinkedIn]([https://www.linkedin.com/in/coequipier2](https://www.linkedin.com/in/nelly-dako-87308a29b?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app))
- **Camus OGOUBIYI** - [GitHub](https://github.com/Camus-OGB) | [LinkedIn](https://www.linkedin.com/in/farid-mamadou-916411277 )

## 📜 Licence
Ce projet est sous licence MIT. Vous êtes libre de le modifier et de l'améliorer.

## 🤝 Contribuer
Les contributions sont les bienvenues !
1. **Fork** le projet 📌
2. **Crée une branche** (`git checkout -b feature-nouvelle-fonctionnalité`)
3. **Commit tes modifications** (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. **Push** sur la branche (`git push origin feature-nouvelle-fonctionnalité`)
5. **Crée une Pull Request** 🎉

