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
