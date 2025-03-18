import sqlite3
from sqlite3 import Error

DATABASE = 'products.db'

def create_connection():
    """Create a database connection."""
    conn = None
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except Error as e:
        print(f"Error: {e}")
    return conn

def create_table():
    """Create the products table if it doesn't exist."""
    conn = create_connection()
    if conn:
        try:
            query = '''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                price REAL NOT NULL
            );
            '''
            conn.execute(query)
            conn.commit()
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

def insert_default_products():
    """Insert two products if the table is empty."""
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM products")
            count = cursor.fetchone()[0]
            
            if count == 0:  # Insert only if table is empty
                query = '''
                INSERT INTO products (name, price) VALUES 
                ('Laptop', 50000),
                ('Smartphone', 20000);
                '''
                cursor.execute(query)
                conn.commit()
                print("✅ Default products added successfully.")
            else:
                print("✅ Products already exist. Skipping insert.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    create_table()
    insert_default_products()
