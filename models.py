"""
Database models and initialization for Smart Price Hunter
"""

import sqlite3
from datetime import datetime
import os

DB_PATH = 'pricehunter.db'

def init_database():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Create the searches table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS searches (
            id TEXT PRIMARY KEY,
            query TEXT NOT NULL,
            timestamp TEXT,
            duration REAL,
            sites TEXT,
            status TEXT DEFAULT 'completed',
            total_products INTEGER DEFAULT 0,
            available_products INTEGER DEFAULT 0
        )
        ''')
        
        # Create the products table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            search_id TEXT,
            name TEXT,
            price REAL,
            original_price REAL,
            site TEXT,
            available INTEGER DEFAULT 1,
            rating REAL,
            review_count INTEGER DEFAULT 0,
            discount_percentage REAL DEFAULT 0,
            savings REAL DEFAULT 0,
            brand TEXT,
            image_url TEXT,
            product_url TEXT,
            extraction_time TEXT,
            FOREIGN KEY(search_id) REFERENCES searches(id)
        )
        ''')
        
        # Create index for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_search_id ON products(search_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_site ON products(site)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_price ON products(price)')
        
        conn.commit()
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
    finally:
        conn.close()

def get_connection():
    """Get database connection"""
    return sqlite3.connect(DB_PATH)

def close_connection(conn):
    """Close database connection safely"""
    if conn:
        conn.close()

# Initialize database when module is imported
if __name__ == "__main__":
    init_database()
else:
    # Auto-initialize when imported
    try:
        init_database()
    except Exception as e:
        print(f"Warning: Could not initialize database: {e}")
