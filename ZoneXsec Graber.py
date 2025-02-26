import undetected_chromedriver as uc
from bs4 import BeautifulSoup
import time
import random

BASE_URLS = {
    "special": "https://zone-xsec.com/special/page={}",
    "archive": "https://zone-xsec.com/archive/page={}",
    "onhold": "https://zone-xsec.com/onhold/page={}"
}

OUTPUT_FILES = {
    "special": "special.txt",
    "archive": "archive.txt",
    "onhold": "onhold.txt"
}

def scrape_with_browser(category):
    url_pattern = BASE_URLS[category]
    output_file = OUTPUT_FILES[category]

    options = uc.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-dev-shm-usage")

    driver = uc.Chrome(options=options)

    page = 1
    while True:
        url = url_pattern.format(page)
        print(f"Scraping {url}...")

        try:
            driver.get(url)
            time.sleep(random.uniform(5, 8))  # Tunggu DDoS challenge selesai

            soup = BeautifulSoup(driver.page_source, "html.parser")
            rows = soup.select("tbody tr")

            if not rows:
                print(f"No more data found for {category}, stopping.")
                break

            with open(output_file, "a") as f:
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) >= 9:
                        defaced_site = columns[8].text.strip()
                        if defaced_site:
                            f.write(defaced_site + "\n")
                            print(f"Saved: {defaced_site}")

            page += 1
        except Exception as e:
            print(f"Error: {e}")
            break

    driver.quit()

def main():
    print("Pilih kategori scraping:")
    print("1 > Special Deface")
    print("2 > Archive")
    print("3 > OnHold")

    choice = input("Masukkan pilihan (1/2/3): ").strip()

    if choice == "1":
        scrape_with_browser("special")
    elif choice == "2":
        scrape_with_browser("archive")
    elif choice == "3":
        scrape_with_browser("onhold")
    else:
        print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
