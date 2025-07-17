from src.api.database import get_db
from src.api import schemas
from typing import List, Optional
import logging

logging.basicConfig(level=logging.INFO)


def get_top_products(limit: int = 10) -> List[schemas.TopProduct]:
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT word, COUNT(*) as count
            FROM (
                SELECT unnest(string_to_array(lower(raw_json->>'text'), ' ')) as word
                FROM raw_marts.fct_messages
                WHERE raw_json->>'text' IS NOT NULL
            ) words
            WHERE length(word) > 3
            GROUP BY word
            ORDER BY count DESC
            LIMIT %s
        ''', (limit,))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [schemas.TopProduct(product=row[0], count=row[1]) for row in rows]
    except Exception as e:
        logging.error(f"Error in get_top_products: {e}")
        raise

def get_channel_activity(channel_name: str) -> Optional[schemas.ChannelActivity]:
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT COUNT(*) FROM raw_marts.fct_messages m
            JOIN raw_marts.dim_channels c ON m.channel_id = c.channel_id
            WHERE c.channel_name = %s
        ''', (channel_name,))
        row = cur.fetchone()
        total_messages = row[0] if row else 0
        cur.execute('''
            SELECT d.date, COUNT(*)
            FROM raw_marts.fct_messages m
            JOIN raw_marts.dim_channels c ON m.channel_id = c.channel_id
            JOIN raw_marts.dim_dates d ON m.date_id = d.date_id
            WHERE c.channel_name = %s
            GROUP BY d.date
            ORDER BY d.date
        ''', (channel_name,))
        messages_per_day = [{'date': str(row[0]), 'count': row[1]} for row in cur.fetchall()]
        cur.close()
        conn.close()
        if total_messages == 0:
            return None
        return schemas.ChannelActivity(
            channel_name=channel_name,
            total_messages=total_messages,
            messages_per_day=messages_per_day
        )
    except Exception as e:
        logging.error(f"Error in get_channel_activity: {e}")
        raise

def search_messages(query: str) -> List[schemas.MessageSearchResult]:
    try:
        conn = get_db()
        cur = conn.cursor()
        cur.execute('''
            SELECT m.message_id, c.channel_name, m.message_date, m.raw_json->>'text' as text
            FROM raw_marts.fct_messages m
            JOIN raw_marts.dim_channels c ON m.channel_id = c.channel_id
            WHERE m.raw_json->>'text' ILIKE %s
            ORDER BY m.message_date DESC
            LIMIT 50
        ''', (f'%{query}%',))
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [schemas.MessageSearchResult(
            message_id=row[0],
            channel_name=row[1],
            message_date=str(row[2]),
            text=row[3]
        ) for row in rows]
    except Exception as e:
        logging.error(f"Error in search_messages: {e}")
        raise