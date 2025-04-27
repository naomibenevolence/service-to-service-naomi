import subprocess
import time
import sys
import os

def run_service(script_path, port):
    # Buat folder database jika belum ada
    if not os.path.exists("database"):
        os.makedirs("database")
        
    # Buat file database.db jika belum ada
    if not os.path.exists("database/app.db"):
        open("database/app.db", "w").close()
        print("File database/app.db berhasil dibuat")
        
    try:
        subprocess.Popen([sys.executable, script_path])
        print(f"Service berjalan di port {port}")
    except Exception as e:
        print(f"Error menjalankan service di port {port}: {str(e)}")

if __name__ == "__main__":
    print("Memulai semua service...")
    
    # Jalankan UserService di port 5000
    run_service("users/user.py", 5000)
    time.sleep(2)  # Tunggu 2 detik
    
    print("\nSemua service telah berjalan!")
    print("UserService: http://localhost:5000")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nMenghentikan semua service...")
