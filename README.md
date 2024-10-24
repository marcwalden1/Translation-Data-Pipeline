# Translation Data Pipeline

This is a prototype of a translation data pipeline with real-time processing and caching, built using Flask, SQLite, Redis, and mock translations.

## Features:
- Real-time translation API
- Caching with Redis for frequently translated phrases
- Language detection with `langdetect`
- Mock translations stored in SQLite

## Requirements

- Python 3.11+
- Redis (running locally)
- Required Python packages (listed in `requirements.txt`)

## Installation

1. Clone this repository or extract the provided ZIP file.
2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
