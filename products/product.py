from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL
        )
    """)
    
    # Insert dummy data for products
    cursor.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (1, 'Laptop Asus', 8000000)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (2, 'HP Xiaomi', 3000000)")
    cursor.execute("INSERT OR IGNORE INTO products (id, name, price) VALUES (3, 'Mouse Rexus', 200000)")
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Selamat datang di ProductService!",
        "endpoints": {
            "GET /products": "Mengambil semua produk",
            "GET /products/<id>": "Mengambil produk berdasarkan id"
        }
    })

@app.route("/products", methods=["GET", "POST"])
@app.route("/products/<int:product_id>", methods=["GET"])
def get_products(product_id=None):
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        price = data.get("price")
        
        if not name or not price:
            return jsonify({"error": "Name dan price harus diisi"}), 400
            
        cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (name, price))
        conn.commit()
        
        new_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            "message": "Produk berhasil ditambahkan",
            "product": {
                "id": new_id,
                "name": name,
                "price": price
            }
        }), 201
    
    if product_id:
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        conn.close()
        if product:
            return jsonify({"id": product[0], "name": product[1], "price": product[2]})
        return jsonify({"error": "Product tidak ditemukan"}), 404
    else:
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()
        conn.close()
        result = [{"id": product[0], "name": product[1], "price": product[2]} for product in products]
        return jsonify(result)

if __name__ == "__main__":
    app.run(port=5001)
