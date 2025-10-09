import sqlite3
from datetime import datetime

DB_PATH = 'pricehunter.db'

def save_search(search_id: str, query: str, sites: list, start_time: datetime, duration: float):
    """Insert a new search record into the searches table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = start_time.isoformat()
    sites_str = ','.join(sites)
    cursor.execute('''
        INSERT OR REPLACE INTO searches (id, query, timestamp, duration, sites)
        VALUES (?, ?, ?, ?, ?)
    ''', (search_id, query, timestamp, duration, sites_str))
    conn.commit()
    conn.close()

def save_products(search_id: str, products: list):
    """
    Insert product records into the products table.
    products: list of dicts with keys: name, price, site, available (bool), extraction_time (datetime)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    for p in products:
        extraction = p['extraction_time']
        if hasattr(extraction, 'isoformat'):
            extraction = extraction.isoformat()
        cursor.execute('''
            INSERT INTO products (search_id, name, price, site, available, extraction_time)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (search_id, p['name'], p['price'], p['site'], int(p['available']), extraction))
    conn.commit()
    conn.close()
