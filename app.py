import csv
import os
import uuid
from datetime import datetime
from pathlib import Path

import requests
from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')

# Common language list shown in the UI.
LANGUAGES = {
    'af': 'Afrikaans',
    'ar': 'Arabic',
    'bn': 'Bengali',
    'bg': 'Bulgarian',
    'ca': 'Catalan',
    'zh-Hans': 'Chinese (Simplified)',
    'zh-Hant': 'Chinese (Traditional)',
    'hr': 'Croatian',
    'cs': 'Czech',
    'da': 'Danish',
    'nl': 'Dutch',
    'en': 'English',
    'et': 'Estonian',
    'fi': 'Finnish',
    'fr': 'French',
    'de': 'German',
    'el': 'Greek',
    'gu': 'Gujarati',
    'he': 'Hebrew',
    'hi': 'Hindi',
    'hu': 'Hungarian',
    'id': 'Indonesian',
    'it': 'Italian',
    'ja': 'Japanese',
    'kn': 'Kannada',
    'ko': 'Korean',
    'lv': 'Latvian',
    'lt': 'Lithuanian',
    'ms': 'Malay',
    'ml': 'Malayalam',
    'mr': 'Marathi',
    'no': 'Norwegian',
    'fa': 'Persian',
    'pl': 'Polish',
    'pt': 'Portuguese',
    'pa': 'Punjabi',
    'ro': 'Romanian',
    'ru': 'Russian',
    'sr-Cyrl': 'Serbian (Cyrillic)',
    'sk': 'Slovak',
    'sl': 'Slovenian',
    'es': 'Spanish',
    'sv': 'Swedish',
    'ta': 'Tamil',
    'te': 'Telugu',
    'th': 'Thai',
    'tr': 'Turkish',
    'uk': 'Ukrainian',
    'ur': 'Urdu',
    'vi': 'Vietnamese'
}

TRANSLATOR_KEY = os.getenv('AZURE_TRANSLATOR_KEY', '')
TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT', 'https://api.cognitive.microsofttranslator.com')
TRANSLATOR_REGION = os.getenv('AZURE_TRANSLATOR_REGION', '')
CONTACT_FILE = Path(os.getenv('CONTACT_STORAGE_FILE', 'contact_messages.csv'))


def azure_translate(text: str, from_lang: str, to_lang: str):
    if not TRANSLATOR_KEY or not TRANSLATOR_REGION:
        raise RuntimeError('Azure Translator environment variables are missing.')

    path = '/translate'
    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': [to_lang],
    }
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_REGION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
    }
    body = [{'text': text}]
    response = requests.post(
        TRANSLATOR_ENDPOINT.rstrip('/') + path,
        params=params,
        headers=headers,
        json=body,
        timeout=25,
    )
    response.raise_for_status()
    data = response.json()
    return data[0]['translations'][0]['text']


@app.route('/')
def home():
    return render_template('index.html', languages=LANGUAGES)


@app.post('/api/translate')
def translate_api():
    payload = request.get_json(silent=True) or {}
    text = (payload.get('text') or '').strip()
    from_lang = payload.get('from') or 'en'
    to_lang = payload.get('to') or 'es'

    if not text:
        return jsonify({'ok': False, 'error': 'Please enter text to translate.'}), 400
    if from_lang == to_lang:
        return jsonify({'ok': False, 'error': 'Please choose two different languages.'}), 400

    try:
        translated_text = azure_translate(text, from_lang, to_lang)
        return jsonify({'ok': True, 'translatedText': translated_text})
    except requests.HTTPError as exc:
        detail = exc.response.text if exc.response is not None else str(exc)
        return jsonify({'ok': False, 'error': f'Translation service error: {detail}'}), 502
    except Exception as exc:
        return jsonify({'ok': False, 'error': str(exc)}), 500


@app.post('/api/contact')
def contact_api():
    payload = request.get_json(silent=True) or {}
    name = (payload.get('name') or '').strip()
    email = (payload.get('email') or '').strip()
    message = (payload.get('message') or '').strip()

    if not name or not email or not message:
        return jsonify({'ok': False, 'error': 'Please complete all contact form fields.'}), 400

    file_exists = CONTACT_FILE.exists()
    with CONTACT_FILE.open('a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['timestamp_utc', 'name', 'email', 'message'])
        writer.writerow([datetime.utcnow().isoformat(), name, email, message])

    return jsonify({'ok': True, 'message': 'Thanks for reaching out. Your message has been saved.'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')), debug=True)