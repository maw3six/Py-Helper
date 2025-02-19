import requests
import random
import time
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# Daftar User-Agent agar tidak terdeteksi bot
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/118.0",
]

# Gunakan set() dengan lock agar tidak ada duplikasi di multi-threading
visited = set()
visited_lock = threading.Lock()

def scrape_directory(url, base_path=""):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    
    try:
        time.sleep(random.uniform(0.5, 2))  # Delay acak agar tidak terdeteksi bot
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a")

        sub_dirs = []
        for link in links:
            href = link.get("href")
            if href and not href.startswith("?") and href not in ["../"]:  # Hindari ".."
                full_path = urljoin(url, href)

                if href.endswith("/"):  # Hanya folder
                    with visited_lock:
                        if full_path not in visited:
                            visited.add(full_path)
                            sub_dirs.append((full_path, base_path + href))

        return sub_dirs  # Return daftar folder yang perlu dikunjungi

    except requests.exceptions.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return []

def process_directory(url, base_path, executor):
    sub_dirs = scrape_directory(url, base_path)
    futures = []

    for full_path, sub_path in sub_dirs:
        futures.append(executor.submit(process_directory, full_path, sub_path, executor))  # Rekursif multi-thread

    return futures

def process_url_list(file_path):
    with open(file_path, "r") as file:
        urls = [line.strip() for line in file if line.strip()]

    with ThreadPoolExecutor(max_workers=5) as executor:  # Gunakan 5 thread untuk URL utama
        url_futures = []
        for base_url in urls:
            if not base_url.endswith("/"):
                base_url += "/"
            url_futures.append(executor.submit(process_directory, base_url, "", executor))

    # Simpan hasilnya ke file tanpa duplikat
    with open("mass_directory_list.txt", "w") as f:
        for path in sorted(visited):
            f.write(path + "\n")

    print("Scraping selesai! Hasil disimpan di mass_directory_list.txt")

if __name__ == "__main__":
    file_path = input("Masukkan nama file daftar URL (.txt): ").strip()
    process_url_list(file_path)
