import os
import json
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Load environment variables
load_dotenv()

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5433')
DB_NAME = os.getenv('DB_NAME', 'kara')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD')

RAW_DATA_PATH = Path(__file__).parent.parent / 'data' / 'raw' / 'telegram_messages'
CHANNELS = ['lobelia4cosmetics', 'tikvahpharma']

CREATE_SCHEMA_SQL = """
CREATE SCHEMA IF NOT EXISTS raw;
"""

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw.{table_name} (
    id SERIAL PRIMARY KEY,
    message_id BIGINT,
    date TIMESTAMP,
    text TEXT,
    image_path TEXT,
    raw_json JSONB
);
"""

INSERT_SQL = """
INSERT INTO raw.{table_name} (message_id, date, text, image_path, raw_json)
VALUES (%s, %s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def extract_fields(json_data):
    message_id = json_data.get('message_id') or json_data.get('id')
    date = json_data.get('date')
    text = json_data.get('text')
    image_path = json_data.get('image_path') or json_data.get('image')
    return message_id, date, text, image_path

def main():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = True
        cur = conn.cursor()
        logging.info('Connected to PostgreSQL')

        # Create schema
        cur.execute(CREATE_SCHEMA_SQL)
        logging.info('Ensured raw schema exists')

        for channel in CHANNELS:
            table_name = channel
            # Create table for channel
            cur.execute(sql.SQL(CREATE_TABLE_SQL).format(table_name=sql.Identifier(table_name)))
            logging.info(f'Ensured table raw.{table_name} exists')

            # Find all JSON files for this channel
            for date_dir in RAW_DATA_PATH.glob('*'):
                channel_dir = date_dir / channel
                if not channel_dir.exists():
                    continue
                for json_file in channel_dir.glob('*.json'):
                    try:
                        with open(json_file, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                        message_id, date, text, image_path = extract_fields(data)
                        # Insert row
                        cur.execute(
                            sql.SQL(INSERT_SQL).format(table_name=sql.Identifier(table_name)),
                            (message_id, date, text, image_path, json.dumps(data))
                        )
                        logging.info(f'Inserted {json_file} into raw.{table_name}')
                    except Exception as e:
                        logging.error(f'Error processing {json_file}: {e}')

        cur.close()
        conn.close()
        logging.info('Done loading all data.')
    except Exception as e:
        logging.error(f'Failed to load data: {e}')

if __name__ == '__main__':
    main()