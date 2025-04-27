## Biodata Developer

- NAMA    : Naomi Benevolence Santoso
- NIM     : 1204220027

---

# 📦 Service-to-Service Communication with Flask

## 📝 Deskripsi Proyek

Proyek ini merupakan implementasi dari sistem integrasi antar layanan (Service-to-Service Communication) menggunakan **Flask**. Terdapat tiga layanan utama yang berjalan secara terpisah:

- **UserService** (Port 5000): Menyediakan data pengguna.
- **ProductService** (Port 5001): Menyediakan data produk.
- **OrderService** (Port 5002): Mengelola pembuatan dan penampilan data pesanan.

Setiap layanan berperan sebagai **provider** dan/atau **consumer**, dan saling berkomunikasi secara langsung menggunakan HTTP dan JSON.

---

## 🚀 Cara Menjalankan Aplikasi

1. **Kloning atau download** project ini.
2. Pastikan sudah menginstal dependensi yang diperlukan:
   ```bash
   pip install flask requests
   ```
3. Jalankan aplikasi:
   ```bash
   python app.py
   ```
4. Aplikasi akan menjalankan ketiga service secara otomatis:
   - UserService: http://localhost:5000
   - ProductService: http://localhost:5001
   - OrderService: http://localhost:5002

---

## 📌 Endpoint API

### 🔹 UserService (Port 5000)

- **GET /**
  - Menampilkan informasi service dan endpoint yang tersedia

- **GET /users/<id>**
  - Mengambil data user berdasarkan `id`.
  - Contoh Response:
    ```json
    {
      "id": 1,
      "name": "Bambang"
    }
    ```

- **POST /users**
  - Mendaftarkan user baru dengan input `name`.
  - Contoh Request:
    ```json
    {
      "name": "Bob"
    }
    ```
  - Contoh Response:
    ```json
    {
      "id": 2,
      "name": "Bob"
    }
    ```

### 🔹 ProductService (Port 5001)

- **GET /**
  - Menampilkan informasi service dan endpoint yang tersedia

- **GET /products**
  - Mengambil daftar semua produk yang tersedia.
  - Contoh Response:
    ```json
    [
      {
        "id": 1,
        "name": "Laptop Asus",
        "price": 8000000
      },
      {
        "id": 2,
        "name": "HP Xiaomi",
        "price": 3000000
      }
    ]
    ```

- **GET /products/<id>**
  - Mengambil data produk berdasarkan `id`.
  - Contoh Response:
    ```json
    {
      "id": 1,
      "name": "Laptop Asus",
      "price": 8000000
    }
    ```

- **POST /products**
  - Mendaftarkan produk baru.
  - Contoh Request:
    ```json
    {
      "name": "Monitor LG",
      "price": 2500000
    }
    ```
  - Contoh Response:
    ```json
    {
      "message": "Produk berhasil ditambahkan",
      "product": {
        "id": 4,
        "name": "Monitor LG", 
        "price": 2500000
      }
    }
    ```

### 🔹 OrderService (Port 5002)

- **GET /**
  - Menampilkan informasi service dan endpoint yang tersedia

- **POST /orders**
  - Membuat pesanan berdasarkan `user_id` dan `product_id`.
  - Contoh Request:
    ```json
    {
      "user_id": 1,
      "product_id": 1
    }
    ```
  - Contoh Response:
    ```json
    {
      "order_id": 1,
      "user": {"id": 1, "name": "Bambang"},
      "product": {"id": 1, "name": "Laptop Asus", "price": 8000000}
    }
    ```

- **GET /orders**
  - Mengambil semua pesanan yang telah dibuat.
  - Contoh Response:
    ```json
    [
      {
        "order_id": 1,
        "user": {"id": 1, "name": "Bambang"},
        "product": {"id": 1, "name": "Laptop Asus", "price": 8000000}
      }
    ]
    ```

---

## 🧠 Arsitektur & Alur Komunikasi

- Setiap service berjalan secara independen di port yang berbeda
- Saat membuat pesanan:
  - **OrderService** bertindak sebagai *consumer*, mengambil data dari **UserService** dan **ProductService** melalui HTTP request
  - Kemudian menyimpan dan menyajikan data transaksi sebagai *provider*
- Semua data disimpan dalam database SQLite yang terpusat

---

## 📄 Lisensi

Proyek ini dibuat untuk keperluan tugas UTS Mata Kuliah **Enterprise Application Integration**.

---
