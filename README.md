# Translation Data Pipeline

This is a prototype of a translation data pipeline with real-time processing and caching, built using Flask, SQLite, Redis, and mock translations.

## Features
- Real-time translation API
- Caching with Redis for frequently translated phrases
- Language detection using `langdetect`
- Mock translations stored in SQLite

## Requirements
- Python 3.11+
- Redis (running locally)
- Required Python packages (listed in `requirements.txt`)

## Installation and Setup

### 1. Clone the Repository:
To get started, clone this repository to your local machine:

```bash
git clone https://github.com/marcwalden1/Translation_Data_Pipeline.git
cd Translation_Data_Pipeline 
```

### 2. Set Up a Virtual Environment:
It’s recommended to use a virtual environment to manage dependencies. You can set it up as follows:

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies:
Install the required Python packages from the requirements.txt file:

```bash
pip install -r requirements.txt
```

### 4. Start Redis:
Make sure Redis is installed and running locally. If not installed, follow instructions from the Redis documentation to set it up.

To start Redis:

```bash
redis-server
```

### 5. Run the Application:
Once Redis is running, you can start the Flask application:

``` bash
python app.py
```

### 6. API Usage
## Translation Endpoint
You can send a POST request to /translate with the text you want to translate.

Example:
``` bash
curl -X POST http://127.0.0.1:5000/translate \
     -H "Content-Type: application/json" \
     -d '{"text": "Hola, ¿cómo estás?"}'
```

Response:
```json

{
  "detected_language": "es",
  "received_text": "Hola, ¿cómo estás?",
  "translated_text": "Hello, how are you?",
  "status": "success"
}
```
