from flask import Flask, redirect, request
import requests
import base64
import hashlib
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

CLIENT_ID = os.getenv("HELLOASSO_CLIENT_ID")
CLIENT_SECRET = os.getenv("HELLOASS_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")
AUTH_URL = "https://auth.helloasso.com/oauth2/authorize"
TOKEN_URL = "https://api.helloasso.com/oauth2/token"

ORGANIZATION_SLUG = os.getenv("HELLOASSO_ORG", "scorpi-burger")  # À adapter si nécessaire

PKCE_STORE = {}

def generate_pkce():
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

@app.route("/")
def index():
    return '<a href="/login">Se connecter via HelloAsso</a>'

@app.route("/login")
def login():
    code_verifier, code_challenge = generate_pkce()
    state = secrets.token_urlsafe(16)
    PKCE_STORE[state] = code_verifier

    auth_url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}"
        f"&response_type=code&code_challenge={code_challenge}&code_challenge_method=S256&state={state}"
    )
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    code_verifier = PKCE_STORE.get(state)

    if not code or not code_verifier:
        return "Erreur : code ou état manquant."

    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "code_verifier": code_verifier
    }

    response = requests.post(TOKEN_URL, data=data)
    if not response.ok:
        return f"<h2>❌ Erreur d'authentification</h2><pre>{response.text}</pre>", 400

    tokens = response.json()
    access_token = tokens.get("access_token")

    # Appel API HelloAsso pour récupérer les formulaires
    headers = {"Authorization": f"Bearer {access_token}"}
    forms_url = f"https://api.helloasso.com/v5/organizations/{ORGANIZATION_SLUG}/forms"
    forms_response = requests.get(forms_url, headers=headers)

    if not forms_response.ok:
        return f"<h2>❌ Erreur API HelloAsso</h2><pre>{forms_response.text}</pre>", 400

    forms = forms_response.json().get("data", [])

    html = """
    <h2>✅ Connexion réussie</h2>
    <p><strong>Token sécurisé (caché ici)</strong></p>
    <h3>📋 Liste des formulaires HelloAsso :</h3>
    <ul>
    """

    for form in forms:
        title = form.get("title", "Sans titre")
        slug = form.get("formSlug", "")
        form_type = form.get("formType", "")
        html += f"<li><strong>{title}</strong> ({form_type}) — <code>Slug</code> : {slug}</li>"

    html += "</ul>"
    html += "<hr><p><em>Projet HelloAsso Suite - by fqz-coder</em></p>"
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
