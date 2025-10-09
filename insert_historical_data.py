import sqlite3

conn = sqlite3.connect('pricehunter.db')
cursor = conn.cursor()

# Insert historical search
cursor.execute("""
    INSERT INTO searches (id, query, timestamp, duration, sites)
    VALUES (?, ?, ?, ?, ?)
""", ('hist_shoes_20250906', 'shoes', '2025-09-06T10:00:00', 2.0, 'amazon,flipkart'))

# Insert historical products
products = [
    ('hist_shoes_20250906', 'shoes - Demo Old', 1299.0, 'Amazon India', 1, '2025-09-06T10:00:10'),
    ('hist_shoes_20250906', 'shoes - Demo Old', 1399.0, 'Flipkart', 1, '2025-09-06T10:00:12'),
]
cursor.executemany("""
    INSERT INTO products (search_id, name, price, site, available, extraction_time)
    VALUES (?, ?, ?, ?, ?, ?)
""", products)

conn.commit()
conn.close()
print("Historical data inserted.")
