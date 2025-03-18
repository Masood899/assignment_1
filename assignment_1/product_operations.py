import sqlite3
from db import create_connection

def add_product(name, price):
    """Add a new product to the database."""
    conn = create_connection()
    try:
        query = 'INSERT INTO products (name, price) VALUES (?, ?)'
        conn.execute(query, (name, price))
        conn.commit()
        print(f"Product '{name}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Error: Product '{name}' already exists.")
    finally:
        conn.close()

def list_products():
    """Retrieve and return all products."""
    conn = create_connection()
    cursor = conn.execute('SELECT * FROM products')
    products = cursor.fetchall()
    conn.close()
    return products

def update_product_price(product_id, new_price):
    """Update the price of a product."""
    conn = create_connection()
    cursor = conn.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    if cursor.fetchone():
        conn.execute('UPDATE products SET price = ? WHERE id = ?', (new_price, product_id))
        conn.commit()
        print("Product price updated successfully.")
    else:
        print("Error: Product not found.")
    conn.close()

def apply_discount(percentage):
    """Apply a discount to all products."""
    conn = create_connection()
    try:
        cursor = conn.cursor()
        query = 'UPDATE products SET price = ROUND(price - (price * ? / 100), 2)'
        cursor.execute(query, (percentage,))
        conn.commit()  # 🔥 Ensure changes are committed
        print(f"✅ {percentage}% discount applied successfully.")
    except Exception as e:
        print(f"❌ Error applying discount: {e}")
    finally:
        conn.close()
