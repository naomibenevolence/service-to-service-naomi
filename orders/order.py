from flask import Flask, request, jsonify
import sqlite3
import requests

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    """)
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Selamat datang di OrderService!",
        "endpoints": {
            "POST /orders": "Membuat pesanan baru",
            "GET /orders": "Mengambil semua pesanan"
        }
    })

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.get_json()
    user_id = data.get("user_id")
    product_id = data.get("product_id")

    # Check if user exists
    user_response = requests.get(f"http://localhost:5000/users/{user_id}")
    if user_response.status_code != 200:
        return jsonify({"error": "Pengguna tidak ditemukan"}), 404

    # Check if product exists
    product_response = requests.get(f"http://localhost:5001/products/{product_id}")
    if product_response.status_code != 200:
        return jsonify({"error": "Produk tidak ditemukan"}), 404

    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, product_id) VALUES (?, ?)", (user_id, product_id))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "order_id": order_id,
        "user": user_response.json(),
        "product": product_response.json()
    }), 201

@app.route("/orders", methods=["GET"])
def list_orders():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT orders.order_id, users.id, users.name, products.id, products.name, products.price
        FROM orders
        JOIN users ON orders.user_id = users.id
        JOIN products ON orders.product_id = products.id
    """)
    orders = cursor.fetchall()
    conn.close()

    result = []
    for order in orders:
        result.append({
            "order_id": order[0],
            "user": {"id": order[1], "name": order[2]},
            "product": {"id": order[3], "name": order[4], "price": order[5]}
        })
    return jsonify(result)

if __name__ == "__main__":
    app.run(port=5002)
