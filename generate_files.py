# generate_files.py
import os

# --- Define the folder structure ---
dirs = [
    "data/raw",
    "dbt_project",
    "src/api",
    "src/enrichment",
    "src/loader",
    "src/orchestration",
    "src/scraper",
]

# --- Define the file structure and their initial content ---
files = {
    ".gitignore": """
# Byte-compiled / optimized / DLL files
__pycache__/
*.pyc
*o
*so

# C extensions
*so

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Installer logs
pip-log.txt
pip-delete-this-directory.txt

# Unit test / coverage reports
htmlcov/
.tox/
.nox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak
venv.bak

# Docker
.dockerignore
docker-compose.yml.override

# project specific
/data/
/dbt_project/logs/
/dbt_project/target/
*.db
*.sqlite3

""",
    "requirements.txt": """
# Core Data and API
fastapi
uvicorn[standard]
sqlalchemy
psycopg2-binary
pandas

# Telegram Scraping
telethon

# Data Transformation
dbt-postgres

# Data Enrichment
ultralytics
torch
torchvision

# Orchestration
dagster
dagster-webserver
dagster-postgres

# Environment Management
python-dotenv
""",
    ".env.example": """
# Telegram API Credentials
TELEGRAM_API_ID=YOUR_API_ID
TELEGRAM_API_HASH=YOUR_API_HASH
TELEGRAM_SESSION_NAME=my_telegram_session

# PostgreSQL Database Credentials
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=medical_data_db
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# dbt Profile Connection Details (can be same as above)
DBT_USER=user
DBT_PASSWORD=password
DBT_HOST=postgres
DBT_PORT=5432
DBT_DBNAME=medical_data_db
DBT_SCHEMA=public
""",
    "Dockerfile": """
# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Set environment variables to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependencies that might be needed for some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install pip requirements
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code to the container
COPY ./src /app/src

# The default command will be to run the FastAPI server.
# This can be overridden in docker-compose.yml for other services like Dagster.
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
""",
    "docker-compose.yml": """
version: '3.8'

services:
  postgres:
    image: postgres:13
    container_name: postgres_db
    env_file:
      - ./.env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 10s
      timeout: 5s
      retries: 5

  app:
    build: .
    container_name: fastapi_app
    env_file:
      - ./.env
    ports:
      - "8000:8000"
    volumes:
      - ./src:/app/src
      - ./data:/app/data
    depends_on:
      postgres:
        condition: service_healthy
    command: uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload

  dagster:
    build: .
    container_name: dagster_ui
    env_file:
      - ./.env
    ports:
      - "3000:3000"
    volumes:
      - ./src:/app/src
      - ./data:/app/data
      - ./dbt_project:/app/dbt_project
    depends_on:
      postgres:
        condition: service_healthy
    command: dagster dev -h 0.0.0.0 -p 3000 -f src/orchestration/definitions.py

volumes:
  postgres_data:
""",
    "README.md": """
# Shipping a Data Product: From Raw Telegram Data to an Analytical API

This project is an end-to-end data pipeline for Telegram, leveraging dbt for transformation, Dagster for orchestration, and YOLOv8 for data enrichment.

## Project Structure

- `data/`: Local data lake for raw JSON files.
- `dbt_project/`: dbt project for data transformation and modeling.
- `src/`: All Python source code.
  - `api/`: FastAPI application.
  - `enrichment/`: YOLO object detection scripts.
  - `loader/`: Scripts to load raw data into PostgreSQL.
  - `orchestration/`: Dagster pipeline definitions.
  - `scraper/`: Telegram scraping scripts.
- `Dockerfile`, `docker-compose.yml`: Containerization setup.
- `requirements.txt`: Python dependencies.

## Setup and Installation

1.  **Initialize Git:**
    ```bash
    git init
    git add .
    git commit -m "Initial project structure setup"
    ```

2.  **Environment Variables:**
    - Copy `.env.example` to a new file named `.env`.
    - Fill in your actual credentials in the `.env` file.
    ```bash
    cp .env.example .env
    ```

3.  **Build and Run with Docker:**
    - This will start the PostgreSQL database, the FastAPI application, and the Dagster UI.
    ```bash
    docker-compose up --build
    ```

4.  **Initialize dbt Project:**
    - Open a new terminal and shell into the `dagster` container (which has all dependencies).
    ```bash
    docker-compose exec dagster bash
    ```
    - Inside the container, navigate to the dbt directory and initialize your project.
    ```bash
    cd dbt_project
    dbt init your_dbt_project_name
    # Follow the prompts, using the credentials from your .env file.
    ```

## Accessing Services

- **PostgreSQL Database:** `localhost:5432`
- **FastAPI Application:** `http://localhost:8000/docs`
- **Dagster UI:** `http://localhost:3000`
""",
    "data/raw/.gitkeep": "",
    "dbt_project/.gitkeep": "",
    "src/__init__.py": "",
    "src/api/__init__.py": "",
    "src/api/main.py": """
from fastapi import FastAPI

app = FastAPI(
    title="Medical Data Insights API",
    description="API for querying analytical data from Telegram channels.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Medical Data Insights API"}

# Placeholder for Task 4 endpoints
# GET /api/reports/top-products?limit=10
# GET /api/channels/{channel_name}/activity
# GET /api/search/messages?query=paracetamol
""",
    "src/api/database.py": "# Database connection logic will go here (e.g., SQLAlchemy setup)",
    "src/api/models.py": "# Pydantic models for request/response validation will go here",
    "src/api/crud.py": "# Functions to interact with the database (CRUD operations) will go here",
    "src/api/schemas.py": "# SQLAlchemy ORM models will go here",
    "src/enrichment/__init__.py": "",
    "src/enrichment/enrich.py": """
# YOLOv8 object detection logic for Task 3 will go here.
def run_enrichment():
    print("Running data enrichment with YOLO...")
    # 1. Scan for new images in the data lake.
    # 2. Load the YOLOv8 model.
    # 3. Process each image and detect objects.
    # 4. Prepare detection results (e.g., message_id, class, score).
    # 5. Load results into the fct_image_detections table in PostgreSQL.
    print("Data enrichment complete.")

if __name__ == "__main__":
    run_enrichment()
""",
    "src/loader/__init__.py": "",
    "src/loader/load_to_pg.py": """
# Logic to load raw JSON from data/raw into PostgreSQL will go here.
def load_raw_data_to_postgres():
    print("Loading raw data to PostgreSQL...")
    # 1. Connect to PostgreSQL.
    # 2. Create a 'raw' schema if it doesn't exist.
    # 3. Find all JSON files in the data/raw directory.
    # 4. For each file, read its content.
    # 5. Insert the JSON content into a raw table (e.g., raw_telegram_messages).
    print("Raw data loading complete.")

if __name__ == "__main__":
    load_raw_data_to_postgres()
""",
    "src/orchestration/__init__.py": "",
    "src/orchestration/definitions.py": """
from dagster import Definitions, load_assets_from_modules

# This is where your Dagster definitions will live.
# For now, it's a placeholder. You will define Jobs, Assets, and Schedules here.

defs = Definitions(
    # assets=all_assets,
    # schedules=[my_schedule],
)
""",
    "src/scraper/__init__.py": "",
    "src/scraper/scrape.py": """
import os
from dotenv import load_dotenv

# Logic for Telegram scraping for Task 1 will go here.

def scrape_telegram_data():
    load_dotenv()
    api_id = os.getenv('TELEGRAM_API_ID')
    api_hash = os.getenv('TELEGRAM_API_HASH')

    print("Starting Telegram scraping process...")
    print(f"Using API ID: {'*' * 5}{api_id[-4:] if api_id else 'Not Set'}") # Avoid printing full key
    
    # 1. Initialize Telethon client.
    # 2. Define the list of channels to scrape.
    # 3. Iterate through channels and fetch messages.
    # 4. Save messages and images to the partitioned data lake (data/raw/...).
    # 5. Implement logging.

    print("Telegram scraping complete.")


if __name__ == "__main__":
    scrape_telegram_data()
""",
}

def create_project_structure():
    """Generates the project folders and files."""
    # Create directories
    for path in dirs:
        try:
            os.makedirs(path)
            print(f"Created directory: {path}")
        except FileExistsError:
            print(f"Directory already exists: {path}")

    # Create files
    for path, content in files.items():
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content.strip())
        print(f"Created file: {path}")

if __name__ == "__main__":
    create_project_structure()
    print("\nProject structure generated successfully!")
    print("Next steps:")
    print("1. Initialize a git repository with 'git init'.")
    print("2. Create a '.env' file from '.env.example' and add your secrets.")
    print("3. Build and run the services using 'docker-compose up --build'.")