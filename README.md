# 🧩 HelloAsso Suite – Projet centralisé

Ce dépôt contient l'ensemble des applications et outils développés autour de HelloAsso pour :

- 🔐 Authentification OAuth
- 🔄 Intégration API (formulaires, participants)
- 🎟️ Lecture & validation de QR codes
- 🧾 Génération de billets et QR codes

---

## 📁 Arborescence

```
helloasso-suite-final/
├── oauth-authentication/       → App Flask pour authentification HelloAsso
├── api-integration-test/       → Tests API HelloAsso (sandbox)
├── qr-ticket-validator/        → Scan QR codes à l'entrée des matchs
├── qr-code-generator/          → Générateur de QR codes par place/billet
```

---

## 🚀 Lancer un projet

1. Ouvre un terminal dans le dossier voulu  
2. Copie le fichier `.env.example` en `.env` et remplis tes identifiants HelloAsso :

```bash
copy .env.example .env     # sous Windows
cp .env.example .env       # sous macOS / Linux
```

3. Lance le projet avec :

```bash
start.bat
```

---

## 🔧 Variables à définir dans `.env`

```env
HELLOASSO_CLIENT_ID=votre_client_id
HELLOASS_SECRET=votre_client_secret
REDIRECT_URI=https://votre-domaine/callback
```

---

## 📌 Besoins

- Python 3.11+
- pip
- (Optionnel) ngrok ou Render pour tests externes avec HelloAsso

---

## 🧑‍💻 Auteur

Projet conçu et maintenu par [@fqz-coder](https://github.com/fqz-coder)
