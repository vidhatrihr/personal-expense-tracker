# Personal Expense Tracker - Backend

A Flask REST API backend with SQLite database integration.

## Architecture

- `routes/` - Route handlers grouped by blueprint (`auth.py`, `expenses.py`)
- `app.py` - Flask application configuration and entry point
- `models.py` - Database models defined using SQLAlchemy
- `populate_db.py` - Script for seeding demo data on initialization
- `requirements.txt` - Python project dependencies

## Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   python app.py
   ```
