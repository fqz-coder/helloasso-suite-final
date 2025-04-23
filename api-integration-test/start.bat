@echo off
echo 📦 Initialisation de l'environnement Python...

IF NOT EXIST venv (
    echo Création de l'environnement virtuel...
    python -m venv venv
)

call venv\Scripts\activate

echo 📦 Installation des dépendances...
pip install -r requirements.txt

echo 🚀 Lancement de l'application...
set FLASK_APP=app.py
set FLASK_ENV=development
flask run --host=0.0.0.0 --port=8000

pause
