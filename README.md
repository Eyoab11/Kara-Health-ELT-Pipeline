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

For more details, see the code and dbt documentation in the project.
=======
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

