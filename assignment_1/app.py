from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DATABASE = "products.db"

def create_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def index():
    return app.send_static_file("index.html")

# 🚀 Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    products = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(products), 200

# 🚀 Add a product
@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (data["name"], data["price"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product added successfully"}), 201

# 🚀 Update a product
@app.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    data = request.json
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET name = ?, price = ? WHERE id = ?", (data["name"], data["price"], id))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product updated successfully"}), 200

# 🚀 Delete a product
@app.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM products WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product deleted successfully"}), 200


@app.route('/api/products/discount', methods=['PUT'])
def apply_discount():
    data = request.json
    discount_percentage = float(data.get("discount", 0))

    if discount_percentage <= 0:
        return jsonify({"message": "Invalid discount percentage"}), 400

    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE products SET price = price - (price * ? / 100)", (discount_percentage,))
    conn.commit()
    conn.close()

    return jsonify({"message": f"Discount of {discount_percentage}% applied successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)
