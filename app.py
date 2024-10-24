import redis
import sqlite3
import unicodedata
import logging
import sys
import time  # To measure response time
from flask import Flask, request, jsonify
from langdetect import detect, LangDetectException


app = Flask(__name__)

# Adjust the Flask app logger
app.logger.setLevel(logging.INFO)

werkzeug_logger = logging.getLogger('werkzeug')
werkzeug_logger.setLevel(logging.INFO)

# Add StreamHandler to Flask logger if necessary
app.logger.addHandler(logging.StreamHandler(sys.stdout))

# Redis connection
cache = redis.Redis(host='localhost', port=6379, db=0)

# Debug Redis connection
try:
    cache.ping()
    app.logger.info("Connected to Redis")
except redis.ConnectionError:
    app.logger.error("Could not connect to Redis")

# Normalize text
def normalize_text(text):
    return unicodedata.normalize('NFKC', text)

# Predefined mock translations
translations = {
    normalize_text("Hola, ¿cómo estás?"): "Hello, how are you?",
    normalize_text("Bonjour tout le monde"): "Hello everyone",
    normalize_text("Guten Morgen"): "Good morning",
    normalize_text("안녕하세요"): "Hello",
    normalize_text("你好"): "Hello",
    normalize_text("おはようございます"): "Good morning"
}

# Initialize the SQLite database
def init_db():
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS translation_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            original_text TEXT,
            detected_language TEXT,
            translated_text TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Fetch translation from the database
def fetch_translation_from_db(text):
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('SELECT translated_text FROM translation_memory WHERE original_text = ?', (text,))
    row = cursor.fetchone()
    conn.close()
    return row[0] if row else None

# Store translation in the database
def store_translation_in_db(original_text, detected_language, translated_text):
    conn = sqlite3.connect('translations.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO translation_memory (original_text, detected_language, translated_text)
        VALUES (?, ?, ?)
    ''', (original_text, detected_language, translated_text))
    conn.commit()
    conn.close()

# Mock translation function
def mock_translate(text):
    normalized_text = normalize_text(text)
    return translations.get(normalized_text, "Translation not available")

@app.route('/translate', methods=['POST'])
def translate_text():
    start_time = time.time()  # Start timing the request

    data = request.get_json()

    if 'text' not in data:
        return jsonify({'error': 'No text provided'}), 400

    input_text = data['text']
    normalized_input_text = normalize_text(input_text)

    # Check if translation exists in the Redis cache
    cached_translation = cache.get(normalized_input_text.encode('utf-8'))
    if cached_translation:
        response_time = time.time() - start_time  # Calculate response time
        app.logger.info(f"Request: '{input_text}', Language: cached, Source: cache, Response time: {response_time:.4f} seconds")
        return jsonify({
            'status': 'success',
            'received_text': input_text,
            'detected_language': 'cached',  # Cached results do not require re-detection
            'translated_text': cached_translation.decode('utf-8'),
            'source': 'cache'
        }), 200

    # Detect the language of the input text
    try:
        detected_language = detect(normalized_input_text)
    except LangDetectException:
        return jsonify({'error': 'Could not detect language'}), 400

    # Fetch translation from database or use mock translation
    translated_text = fetch_translation_from_db(normalized_input_text)
    if translated_text is None:
        translated_text = mock_translate(normalized_input_text)
        store_translation_in_db(normalized_input_text, detected_language, translated_text)

    # Store the translation in Redis cache
    cache.set(normalized_input_text.encode('utf-8'), translated_text)

    response_time = time.time() - start_time  # Calculate response time

    # Log the request details
    app.logger.info(f"Request: '{input_text}', Language: {detected_language}, Source: new translation, Response time: {response_time:.4f} seconds")

    return jsonify({
        'status': 'success',
        'received_text': input_text,
        'detected_language': detected_language,
        'translated_text': translated_text
    }), 200

if __name__ == '__main__':
    init_db()
    app.run(port=5000)  # Remove debug=True

