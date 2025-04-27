from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    # Insert dummy data for users
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (1, 'Bambang')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (2, 'Budi')")
    cursor.execute("INSERT OR IGNORE INTO users (id, name) VALUES (3, 'Ucup')")
    
    conn.commit()
    conn.close()

# Initialize the database
init_db()

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Selamat datang di UserService!",
        "endpoints": {
            "GET /users/<id>": "Mengambil data user berdasarkan id",
            "POST /users": "Mendaftarkan user baru"
        }
    })

@app.route("/users", methods=["POST"])
def register_user():
    data = request.get_json()
    name = data.get("name")

    if not name:
        return jsonify({"error": "Nama tidak boleh kosong"}), 400

    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name) VALUES (?)", (name,))
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({"id": user_id, "name": name}), 201

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    conn = sqlite3.connect("database/app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"id": user[0], "name": user[1]})
    return jsonify({"error": "User tidak ditemukan"}), 404

if __name__ == "__main__":
    app.run(port=5000)
