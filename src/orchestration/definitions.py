from dagster import op, Definitions, job
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "src/scraper/scrape.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/loader/load_to_pg.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dotenv", "run", "--", "dbt", "run"], check=True)
    subprocess.run(["dotenv", "run", "--", "dbt", "test"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/enrichment/enrich.py"], check=True)

@job
def kara_pipeline():
    scrape = scrape_telegram_data()
    load = load_raw_to_postgres()
    dbt = run_dbt_transformations()
    yolo = run_yolo_enrichment()

    load = load.alias("load_raw_to_postgres")(scrape)
    dbt = dbt.alias("run_dbt_transformations")(load)
    yolo = yolo.alias("run_yolo_enrichment")(dbt)

# Register the job in Definitions

defs = Definitions(
    jobs=[kara_pipeline],
)