# Kara-Health-ELT-Pipeline

![alt text](https://img.shields.io/badge/status-Phase%201%20Complete-green)

This project is an end-to-end data pipeline designed to ingest, process, and analyze data from public Ethiopian medical Telegram channels. The goal is to transform unstructured posts into actionable insights, answering key business questions about product trends, pricing, and channel activity as outlined by "Kara Solutions".

This README documents the completion of Phase 1 (Tasks 0 & 1), which focused on building the foundational infrastructure and the data ingestion pipeline.

## Table of Contents
- [Project Architecture (Phase 1)](#project-architecture-phase-1)
- [Key Features & Accomplishments](#key-features--accomplishments)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Set Up Environment Variables](#2-set-up-environment-variables)
  - [3. Build and Run the Environment](#3-build-and-run-the-environment)
  - [4. Run the Data Scraper](#4-run-the-data-scraper)
- [Data Lake Structure](#data-lake-structure)
- [Tools & Technologies Used](#tools--technologies-used)
- [Next Steps](#next-steps)

## Project Architecture (Phase 1)
The first phase of the project established a robust, containerized environment for data ingestion. The workflow is as follows:

## Data Pipeline Flow (Phase 1)

The data flows through the following components in Phase 1:

1. **Telegram API** - Source of raw message data
2. **Python Scraper (Telethon)** - Collects and processes messages
3. **Docker Container** - Containerized execution environment
4. **Partitioned Raw Data Lake** - Organized storage of raw data

All components, including the Python environment and the PostgreSQL database, are managed by Docker to ensure perfect reproducibility.

## Key Features & Accomplishments
This initial phase successfully delivered a production-ready foundation for the data pipeline.

✅ **Reproducible Project Environment (Task 0):**
- The entire application stack is containerized using Docker and Docker Compose.
- A professional project structure separates source code (`src/`), data (`data/`), and configuration.
- All Python dependencies are managed in `requirements.txt`.

✅ **Secure Credential Management (Task 0):**
- Sensitive credentials (API keys, database passwords) are managed securely using a `.env` file.
- The `.gitignore` file is properly configured to prevent committing secrets, session files, and raw data to version control.

✅ **Data Scraping and Collection Pipeline (Task 1):**
- A Python script using Telethon reliably extracts messages and associated images from multiple target Telegram channels.
- The script includes robust error handling and logging to monitor its progress.

✅ **Partitioned Raw Data Lake:**
- The scraper populates a local "data lake" in the `/data/raw` directory.
- Data is stored in a partitioned structure (`YYYY-MM-DD/channel_name/`) for efficient, incremental processing.
- Each message's metadata is preserved in a separate JSON file, and images are stored as `.jpg` files, creating a complete source of truth.

## Getting Started
Follow these steps to set up and run the data ingestion pipeline on your local machine.

### Prerequisites
- Git
- Docker Desktop installed and running.

### 1. Clone the Repository
```bash
git clone https://github.com/[YourGitHubUsername]/Kara-Health-ELT-Pipeline.git
cd Kara-Health-ELT-Pipeline
```
### 2. Set Up Environment Variables
This is the most critical step for connecting to the Telegram API.

### Copy the example environment file:
```bash
cp .env.example .env
```
## Get Telegram API Credentials

1. Log in to [my.telegram.org](https://my.telegram.org)
2. Navigate to "API development tools"
3. Create a new application
4. You'll receive:
   - `api_id`
   - `api_hash`

## Edit Environment File
Replace the placeholders in `.env` with your credentials:

```plaintext
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
```

## 3. Build and Run the Environment

### Start Services
Build and launch the containerized services in detached mode:

```bash
docker-compose up --build -d
```

## 3. Verify Running Containers

### Check Container Status
```bash
docker ps
```

## Expected Running Services

| Icon | Container Name | Description |
|------|----------------|-------------|
| 🐘 | `postgres_db` | PostgreSQL database container |
| 🐍 | `fastapi_app` | Main application container |
| 🧩 | `dagster_ui` | Data pipeline orchestration interface |

---

## Execute Data Scraper

### Access Container
```bash
docker-compose exec fastapi_app bash
```

## 🚀 Run Scraper

```bash
python src/scraper/scrape.py
```

## 🔐 Authentication Process

### Required Credentials:
1. **📱 Phone Number**  
   `+[CountryCode][Number]` (e.g., `+251912345678`)  
   *Include country code with no spaces*

2. **🔒 2FA Password** *(if enabled)*  
   Your Telegram account's two-factor authentication password

3. **✉️ Verification Code**  
   Will be sent to your Telegram app/messages

> 💾 The authentication creates a `.session` file in your project root  
> *This file is automatically excluded from Git via `.gitignore`*

---

## 📂 Data Directory Structure

```text
data/
└── raw/
    └── telegram_messages/
        └── YYYY-MM-DD/                  # Collection date
            ├── channel_name_1/          # Source channel
            │   ├── [message_id].json   # Message metadata
            │   ├── [message_id].jpg    # Attached media
            │   └── [message_id].json
            └── channel_name_2/
                ├── [message_id].json
                └── ...
```

## 🔍 Data Structure Notes

> **Actual directories will contain:**
> - `YYYY-MM-DD` formatted dates (e.g., `2024-03-25`)
> - Exact Telegram channel names (e.g., `ethio_pharma_news`)
> - Telegram's internal message IDs (e.g., `1234567890.json`)

---

## 🛠 Documentation Enhancements

### 🏗 Structural Improvements
```diff
+ ✅ Clear heading hierarchy (H2 → H3 → H4)
+ ✅ Visual section dividers (---) 
+ ✅ Consistent 4-space code indentation
```
## 🎨 Presentation Upgrades

```diff
# Syntax Improvements
+ ✅ Language-specific highlighting (bash/json/text)
+ ✅ Semantic emoji usage (🔍, 🛠, ⚙)
+ ✅ Consistent bullet-point hierarchy
```

## ⚙ Technical Refinements

```diff
# Documentation Enhancements
+ ✅ Complete directory path annotations
+ ✅ Visual authentication workflow diagram
+ ✅ Environment-specific configuration tips
```

## ✨ Readability Features

```diff
# Content Design Improvements
+ ✅ Color-coded alert boxes (💡info/⚠️warning/❗danger)
+ ✅ Consistent monospace formatting (commands, paths, code)
+ ✅ Progressive content disclosure (H2 → H3 → H4)
```

---

# Task 2: Data Modeling and Transformation (Transform)

### What Was Done
- **Raw data** from Telegram channels is loaded into a PostgreSQL `raw` schema.
- **dbt** is used to transform and model this data into a clean, trusted star schema optimized for analytics.
- **Staging models** clean and standardize raw data for each channel.
- **Mart models** implement a star schema:
  - `dim_channels`: Channel dimension
  - `dim_dates`: Date dimension
  - `fct_messages`: Fact table for messages, with metrics and foreign keys
- **Data quality tests** (unique, not_null, and custom business rules) are implemented using dbt's testing framework.
- **Documentation** is generated for all models and columns.

### How to Run the dbt Pipeline
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   dbt deps
   ```
2. **Set up your environment variables** in a `.env` file in the project root:
   ```
   DB_HOST=localhost
   DB_PORT=5433
   DB_NAME=kara
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```
3. **Run dbt models:**
   ```sh
   dotenv run -- dbt run
   ```
4. **Run dbt tests:**
   ```sh
   dotenv run -- dbt test
   ```
5. **Generate and view documentation:**
   ```sh
   dotenv run -- dbt docs generate
   dotenv run -- dbt docs serve --host 127.0.0.1
   ```

### Star Schema Diagram
- **dim_channels** ← **fct_messages** → **dim_dates**

### Notes
- All models and tests are documented in `dbt_project/models/staging/schema.yml`.
- Custom tests ensure data quality and enforce business rules.
- The pipeline is modular and ready for further enrichment and API development.

---

# Task 3: Data Enrichment with Object Detection (YOLO)

### What Was Done
- **YOLOv8 object detection** was used to analyze all images scraped from Telegram channels.
- A Python enrichment script scans all images, runs YOLOv8, and stores detected objects (class, confidence, etc.) in the `raw.image_detections` table in PostgreSQL.
- A new dbt fact model, `fct_image_detections`, links detections to messages, channels, and dates in the star schema.
- Tests and documentation are included for all new columns.

### How to Run Image Enrichment and Update the Warehouse
1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
2. **Run the enrichment script:**
   ```sh
   python src/enrichment/enrich.py
   ```
3. **Update the warehouse with new detections:**
   ```sh
   dotenv run -- dbt run
   dotenv run -- dbt test
   ```
4. **(Optional) Regenerate and view docs:**
   ```sh
   dotenv run -- dbt docs generate
   dotenv run -- dbt docs serve --host 127.0.0.1
   ```

### Notes
- Each detection is linked to its message, channel, and date for rich analytics.
- The pipeline is now ready for advanced analysis and API development.

---

# Task 4: Analytical API (FastAPI)

## Overview
The project exposes a RESTful API using FastAPI to provide analytical insights from the processed Telegram data. The API enables programmatic access to product trends, channel activity, and message search, supporting business intelligence and reporting use cases.

## How to Run the API
1. Ensure the database and all dbt models are up to date (see previous tasks).
2. Start the FastAPI application (if not already running via Docker Compose):
   ```bash
   docker-compose up -d
   # or, if running locally:
   uvicorn src.api.main:app --reload
   ```
3. The API will be available at: `http://localhost:8000`
4. Interactive docs: `http://localhost:8000/docs`

## Available Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/reports/top-products` | GET | Returns the most frequently mentioned words (proxy for products) |
| `/api/channels/{channel_name}/activity` | GET | Returns posting activity for a given channel |
| `/api/search/messages` | GET | Searches messages for a keyword |

---

### 1. Get Top Products
- **Endpoint:** `/api/reports/top-products`
- **Method:** `GET`
- **Query Parameters:**
  - `limit` (optional, int, default=10): Number of top products to return
- **Description:** Returns the most frequently mentioned words in messages (as a proxy for product mentions).
- **Example Request:**
  ```http
  GET /api/reports/top-products?limit=5
  ```
- **Example Response:**
  ```json
  [
    { "product": "paracetamol", "count": 42 },
    { "product": "amoxicillin", "count": 37 },
    { "product": "vitamin", "count": 29 }
  ]
  ```

### 2. Get Channel Activity
- **Endpoint:** `/api/channels/{channel_name}/activity`
- **Method:** `GET`
- **Path Parameters:**
  - `channel_name` (string): Name of the Telegram channel
- **Description:** Returns total messages and daily posting activity for the specified channel.
- **Example Request:**
  ```http
  GET /api/channels/lobelia4cosmetics/activity
  ```
- **Example Response:**
  ```json
  {
    "channel_name": "lobelia4cosmetics",
    "total_messages": 120,
    "messages_per_day": [
      { "date": "2024-07-16", "count": 15 },
      { "date": "2024-07-17", "count": 20 }
    ]
  }
  ```
- **Error Response:**
  ```json
  { "detail": "Channel not found or no activity." }
  ```

### 3. Search Messages
- **Endpoint:** `/api/search/messages`
- **Method:** `GET`
- **Query Parameters:**
  - `query` (string, required): Keyword to search for in messages
- **Description:** Returns up to 50 recent messages containing the search keyword.
- **Example Request:**
  ```http
  GET /api/search/messages?query=paracetamol
  ```
- **Example Response:**
  ```json
  [
    {
      "message_id": 18555,
      "channel_name": "lobelia4cosmetics",
      "message_date": "2024-07-16",
      "text": "Paracetamol 500mg now available!"
    },
    {
      "message_id": 172713,
      "channel_name": "tikvahpharma",
      "message_date": "2024-07-16",
      "text": "Special on paracetamol this week."
    }
  ]
  ```

---

## API Documentation
- Interactive Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

For further details, see the code in `src/api/`.

---

# Task 5: Pipeline Orchestration (Dagster)

## What Was Done
- Introduced [Dagster](https://dagster.io/) for robust, observable, and schedulable pipeline orchestration.
- Defined pipeline steps as Dagster ops:
  - `scrape_telegram_data`: Scrapes Telegram channels for new messages and images.
  - `load_raw_to_postgres`: Loads raw JSON files into PostgreSQL.
  - `run_dbt_transformations`: Runs dbt models and tests to transform and validate data.
  - `run_yolo_enrichment`: Runs YOLOv8 enrichment on images and stores detections.
- Combined all steps into a single Dagster job (`kara_pipeline`) for end-to-end execution.
- Ready for scheduling and monitoring via Dagster's local UI.

## How to Set Up and Use Dagster

### 1. Install Dagster
If not already installed:
```bash
pip install dagster dagster-webserver
```

### 2. Pipeline Definition
- The pipeline is defined in `src/orchestration/definitions.py`.
- Each step is a Dagster op that calls the corresponding script or command.
- The job `kara_pipeline` runs all steps in sequence.

### 3. Launch the Dagster UI
Start the Dagster development UI:
```bash
dagster dev
```
- Access the UI at [http://localhost:3000](http://localhost:3000)
- You can trigger the pipeline manually, inspect logs, and monitor runs.

### 4. Run the Pipeline
- In the Dagster UI, select the `kara_pipeline` job and click "Launch Run" to execute the full pipeline.

### 5. (Optional) Scheduling
- You can add a schedule in `src/orchestration/definitions.py` to run the pipeline automatically (e.g., daily).
- See [Dagster scheduling docs](https://docs.dagster.io/concepts/partitions-schedules-sensors/schedules) for details.

---
