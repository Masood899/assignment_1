import sqlite3

DATABASE = "products.db"

def create_connection():
    """Create a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE)
    return conn

def create_table():
    """Create the products table if it doesn't exist."""
    conn = create_connection()
    query = '''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        price REAL NOT NULL
    );
    '''
    conn.execute(query)
    conn.commit()
    conn.close()

def insert_default_products():
    """Insert default products if the table is empty."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]

    if count == 0:  # Insert only if table is empty
        cursor.execute("INSERT INTO products (name, price) VALUES ('Laptop', 50000), ('Smartphone', 20000)")
        conn.commit()
        print("✅ Default products added successfully.")
    else:
        print("✅ Products already exist. Skipping insert.")

    conn.close()

if __name__ == "__main__":
    create_table()
    insert_default_products()