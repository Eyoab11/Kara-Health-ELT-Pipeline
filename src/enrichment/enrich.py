import os
import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
from ultralytics import YOLO
from pathlib import Path
import logging

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

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS raw.image_detections (
    id SERIAL PRIMARY KEY,
    message_id BIGINT,
    image_path TEXT,
    detected_object_class TEXT,
    confidence_score FLOAT,
    detection_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

INSERT_SQL = """
INSERT INTO raw.image_detections (message_id, image_path, detected_object_class, confidence_score)
VALUES (%s, %s, %s, %s)
ON CONFLICT DO NOTHING;
"""

def get_message_id_from_filename(filename):
    return int(Path(filename).stem)

def main():
    # Load YOLOv8 model (use 'yolov8n.pt' for speed, or 'yolov8s.pt' for better accuracy)
    model = YOLO('yolov8n.pt')
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
        cur.execute(CREATE_TABLE_SQL)
        logging.info('Ensured raw.image_detections table exists')

        # Scan all images
        for date_dir in RAW_DATA_PATH.glob('*'):
            for channel_dir in date_dir.iterdir():
                if not channel_dir.is_dir():
                    continue
                for image_file in channel_dir.glob('*.jpg'):
                    message_id = get_message_id_from_filename(image_file.name)
                    try:
                        results = model(image_file)
                        for r in results:
                            boxes = r.boxes
                            names = r.names
                            for box in boxes:
                                cls_id = int(box.cls[0])
                                detected_class = names[cls_id] if names and cls_id < len(names) else str(cls_id)
                                confidence = float(box.conf[0])
                                cur.execute(
                                    INSERT_SQL,
                                    (message_id, str(image_file), detected_class, confidence)
                                )
                        logging.info(f'Processed {image_file}')
                    except Exception as e:
                        logging.error(f'Error processing {image_file}: {e}')
        cur.close()
        conn.close()
        logging.info('Done with image enrichment.')
    except Exception as e:
        logging.error(f'Failed to enrich images: {e}')

if __name__ == '__main__':
    main()