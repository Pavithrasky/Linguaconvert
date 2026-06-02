# LinguaConvert – Python Language Converter Website

A polished Flask website with three tabs:
- **About**
- **Convert (From → To)**
- **Contact Us**

It includes a meaningful world-inspired background image, a production-ready Flask structure, JavaScript interactions, and cloud deployment files.

## Features
- Python + Flask backend
- Azure Translator REST API integration
- Beautiful glassmorphism UI
- Background SVG artwork included locally
- Contact form saving messages to `contact_messages.csv`
- Ready for cloud hosting with Gunicorn and Docker

## Project structure
```
linguaconvert_webapp/
├── app.py
├── requirements.txt
├── Dockerfile
├── .env.example
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/styles.css
    ├── js/app.js
    └── img/global-harmony.svg
```

## Local run
```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# fill in the Azure Translator values in .env
python app.py
```

Open: `http://127.0.0.1:8000`

## Environment variables
Create a `.env` file using `.env.example`.

Required for translation:
- `AZURE_TRANSLATOR_KEY`
- `AZURE_TRANSLATOR_REGION`
- `AZURE_TRANSLATOR_ENDPOINT` (default provided)

Optional:
- `SECRET_KEY`
- `PORT`
- `CONTACT_STORAGE_FILE`

## Deploy globally (recommended)
This app is structured for **Azure App Service on Linux** or any Docker-compatible host.

### Option A – Azure App Service
1. Create an Azure App Service (Linux, Python runtime).
2. Add the environment variables from `.env.example` into App Settings.
3. Deploy this folder using Azure CLI, VS Code, GitHub Actions, or Azure Developer CLI.
4. Set startup command (if needed):
```bash
gunicorn --bind=0.0.0.0:8000 app:app
```

### Option B – Docker / Container hosting
```bash
docker build -t linguaconvert .
docker run -p 8000:8000 --env-file .env linguaconvert
```

Then deploy the same container image to Azure App Service for Containers, Azure Container Apps, Render, Railway, or another hosting provider.

## Production notes
- Store secrets in hosting platform settings, never in source control.
- Replace the sample contact email address in the HTML.
- Use HTTPS in production.
- Add form spam protection (reCAPTCHA / rate limiting) if public internet traffic is expected.