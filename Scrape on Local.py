import os
import threading
from concurrent.futures import ThreadPoolExecutor

visited = set()  # Set untuk menyimpan path unik
visited_lock = threading.Lock()  # Lock agar multi-thread aman

def crawl_directory(directory):
    """Mencari semua folder & subfolder dalam direktori menggunakan os.walk()."""
    try:
        for root, dirs, _ in os.walk(directory):  # os.walk otomatis masuk ke dalam semua subfolder
            formatted_path = os.path.join(root, "")  # Menambahkan \ di akhir path
            
            with visited_lock:
                if formatted_path not in visited:
                    visited.add(formatted_path)  # Simpan folder unik
                
    except PermissionError:
        print(f"[!] Akses ditolak: {directory}")
    except Exception as e:
        print(f"[!] Error membaca {directory}: {e}")

def process_directory(directory, executor):
    """Jalankan crawling di dalam thread pool executor."""
    executor.submit(crawl_directory, directory)

def scan_single_directory():
    """Scan satu folder input dari user."""
    base_path = input("Masukkan path folder (contoh: C:\\Users\\Public\\): ").strip()

    if not os.path.exists(base_path):
        print("[!] Path tidak ditemukan!")
        return

    with ThreadPoolExecutor(max_workers=10) as executor:
        process_directory(base_path, executor)

    # Simpan hasil ke file
    with open("windows_folders.txt", "w") as f:
        for path in sorted(visited):
            f.write(path + "\n")

    print("[✅] Crawling selesai! Hasil disimpan di windows_folders.txt")

def scan_from_file():
    """Mass scan daftar folder dari file .txt"""
    file_path = input("Masukkan nama file daftar path (.txt): ").strip()

    if not os.path.exists(file_path):
        print("[!] File tidak ditemukan!")
        return

    with open(file_path, "r") as file:
        directories = [line.strip() for line in file if os.path.exists(line.strip())]

    with ThreadPoolExecutor(max_workers=5) as executor:
        for directory in directories:
            executor.submit(crawl_directory, directory)

    # Simpan hasil ke file
    with open("mass_windows_folders.txt", "w") as f:
        for path in sorted(visited):
            f.write(path + "\n")

    print("[✅] Mass crawling selesai! Hasil disimpan di mass_windows_folders.txt")

if __name__ == "__main__":
    print("Pilih Mode Crawling:")
    print("1. Scan satu folder")
    print("2. Scan dari daftar folder di file .txt")
    choice = input("Pilihan (1/2): ").strip()

    if choice == "1":
        scan_single_directory()
    elif choice == "2":
        scan_from_file()
    else:
        print("[!] Pilihan tidak valid!")
