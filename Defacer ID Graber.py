import aiohttp
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import random

BASE_URL_SPECIAL = "https://defacer.id/archive/special/{}"
OUTPUT_SPECIAL = "defacer_special.txt"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:115.0) Gecko/20100101 Firefox/115.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
]

def extract_root_domain(url):
    parsed_url = urlparse(f"http://{url}")
    domain_parts = parsed_url.netloc.split('.')
    if len(domain_parts) > 2:
        return '.'.join(domain_parts[-2:])
    return parsed_url.netloc

async def fetch(session, url):
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    async with session.get(url, headers=headers, timeout=10) as response:
        if response.status == 200:
            return await response.text()
        return None

async def scrape_defaced_urls(seen_domains):
    page = 1
    async with aiohttp.ClientSession() as session:
        while True:
            print(f"Scraping {BASE_URL_SPECIAL.format(page)}...")
            url = BASE_URL_SPECIAL.format(page)
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
            
            with open(OUTPUT_SPECIAL, "a") as f:
                for domain in sorted(new_domains):
                    f.write(domain + "\n")
                    print(f"Saved: {domain}")
            
            page += 1
            await asyncio.sleep(random.uniform(1, 3))
    
    print("Scraping selesai untuk kategori spesial!")

async def main():
    seen_domains = set()
    try:
        with open(OUTPUT_SPECIAL, "r") as f:
            seen_domains.update(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        pass
    
    await scrape_defaced_urls(seen_domains)

if __name__ == "__main__":
    asyncio.run(main())
