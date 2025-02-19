import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random

BASE_URL_ATTACKER = "https://zone-xsec.com/archive/attacker/{}/page={}"
BASE_URL_SPECIAL = "https://zone-xsec.com/special/page={}"
BASE_URL_ARCHIVE = "https://zone-xsec.com/archive/page={}"

ATTACKER_FILE = "attackers.txt"
OUTPUT_ATTACKER = "mass-grab.txt"
OUTPUT_SPECIAL = "special.txt"
OUTPUT_ARCHIVE = "archive.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

def extract_root_domain(url):
    parsed_url = urlparse(f"http://{url}")
    domain_parts = parsed_url.netloc.split('/')
    if len(domain_parts) > 2:
        return '.'.join(domain_parts[-2:])
    return parsed_url.netloc

async def fetch(session, url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    async with session.get(url, headers=headers, timeout=10) as response:
        if response.status == 200:
            return await response.text()
        return None

async def scrape_defaced_urls(url_pattern, seen_domains, output_file):
    page = 1
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Scraping {url_pattern.format(page)}...")
            url = url_pattern.format(page)
            response_text = await fetch(session, url)
            
            if not response_text:
                print(f"Stopping {url}, reached the last page or blocked.")
                break
            
            soup = BeautifulSoup(response_text, "html.parser")
            rows = soup.select("tbody tr")
            
            if not rows:
                print(f"No more defaced sites found, stopping.")
                break
            
            new_domains = set()
            for row in rows:
                columns = row.find_all("td")
                if len(columns) >= 9:
                    defaced_site = columns[8].text.strip()
                    if defaced_site:
                        root_domain = extract_root_domain(defaced_site)
                        if root_domain not in seen_domains:
                            new_domains.add(root_domain)
                            seen_domains.add(root_domain)
            
            with open(output_file, "a") as f:
                for domain in sorted(new_domains):
                    f.write(domain + "\n")
                    print(f"Saved: {domain}")
            
            page += 1
            await asyncio.sleep(random.uniform(1, 3))
    
    print(f"Scraping selesai untuk {url_pattern}!")

async def main():
    print("Pilih opsi scraping:")
    print("1 > Grab By Attacker")
    print("2 > Grab By Special Deface")
    print("3 > Grab By Archive")
    
    choice = input("Masukkan pilihan (1/2/3): ")
    seen_domains = set()
    
    if choice == "1":
        try:
            with open(OUTPUT_ATTACKER, "r") as f:
                seen_domains.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            pass
        with open(ATTACKER_FILE, "r") as f:
            attackers = [line.strip() for line in f if line.strip()]
        tasks = [scrape_defaced_urls(BASE_URL_ATTACKER.format(attacker, "{}"), seen_domains, OUTPUT_ATTACKER) for attacker in attackers]
    elif choice == "2":
        try:
            with open(OUTPUT_SPECIAL, "r") as f:
                seen_domains.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            pass
        tasks = [scrape_defaced_urls(BASE_URL_SPECIAL.format("{}"), seen_domains, OUTPUT_SPECIAL)]
    elif choice == "3":
        try:
            with open(OUTPUT_ARCHIVE, "r") as f:
                seen_domains.update(line.strip() for line in f if line.strip())
        except FileNotFoundError:
            pass
        tasks = [scrape_defaced_urls(BASE_URL_ARCHIVE.format("{}"), seen_domains, OUTPUT_ARCHIVE)]
    else:
        print("Pilihan tidak valid.")
        return
    
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())