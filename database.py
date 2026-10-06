import sqlite3


def get_connection():

    connection = sqlite3.connect("rfqs.db")
    connection.row_factory = sqlite3.Row

    return connection


connection = get_connection()

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS rfqs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        product TEXT,
        quantity INTEGER,
        delivery_date TEXT,
        delivery_location TEXT,
        requirements TEXT
        status TEXT DEFAULT 'NEW',
        unit_price REAL,
        total_price REAL    
    )
""")

connection.commit()
connection.close()


def save_rfq(rfq):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
    INSERT INTO rfqs (
        company,
        product,
        quantity,
        delivery_date,
        delivery_location,
        requirements,
        status
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    rfq["company"],
    rfq["product"],
    rfq["quantity"],
    rfq["delivery_date"],
    rfq["delivery_location"],
    ", ".join(rfq["requirements"]),
    "NEW"
))

    connection.commit()
    connection.close()


def get_rfqs():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM rfqs")

    rfqs = cursor.fetchall()

    connection.close()

    return rfqs

def update_rfq_status(rfq_id, status):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE rfqs
        SET status = ?
        WHERE id = ?
    """, (status, rfq_id))

    connection.commit()
    connection.close()

def get_rfq_stats():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM rfqs
        GROUP BY status
    """)

    results = cursor.fetchall()

    connection.close()

    stats = {
        "NEW": 0,
        "QUOTING": 0,
        "QUOTED": 0,
        "WON": 0,
        "LOST": 0
    }

    for row in results:
        stats[row["status"]] = row["count"]

    stats["TOTAL"] = sum(stats.values())

    return stats

def create_quote(rfq_id, unit_price, total_price):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE rfqs
        SET unit_price = ?, total_price = ?, status = 'QUOTED'
        WHERE id = ?
    """, (unit_price, total_price, rfq_id))

    connection.commit()
    connection.close()
