import requests
import random
import os
from concurrent.futures import ThreadPoolExecutor

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:80.0) Gecko/20100101 Firefox/80.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:37.0) Gecko/20100101 Firefox/37.0',
]

CMS_SIGNS = {
    'PrestaShop': [
        'content="PrestaShop"',
        'class="prestashop"',
        'id="category"',
        '/modules/prestashop/',
    ],
    'OpenCart': [
        'catalog/view/',
        'opencart.js',
        'class="oc-main"',
        'id="footer-open-cart"',
    ],
    'vBulletin': [
        'meta name="generator" content="vBulletin',
        'vbulletin_',
        '<link rel="stylesheet" href="styles/vbulletin',
        'vbulletin.com/forum/',
    ],
    'Drupal': [
        '/sites/default/',
        'Drupal.settings',
        'id="block-drupal-blocks"',
        'theme="drupal"',
    ],
    'Laravel': [
        'laravel_session',
        'X-Powered-By: Laravel',
        'class="laravel"',
        'csrf_token',
    ],
    'WordPress': [
        '/wp-includes/js/jquery/jquery.js',
        'wp-content/',
        '/wp-admin/',
        '<meta name="generator" content="WordPress',
    ],
    'Joomla': [
        '/media/system/js/core.js',
        'Joomla!',
        'joomla.js',
        'generator" content="Joomla',
    ],
    'Magento': [
        'Magento/',
        'X-Magento-Cache',
        '/skin/frontend/',
        '<meta name="generator" content="Magento',
    ],
    'Typo3': [
        r'TYPO3\CMS',
        '/typo3conf/ext/',
        '<meta name="generator" content="TYPO3 CMS',
        'TYPO3',
    ],
    'Shopify': [
        '/cdn.shopify.com/',
        '<meta name="generator" content="Shopify',
        'class="shopify-section"',
        'Shopify.shop',
    ],
    'Dead Site': [],
}

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def check_cms(site, session):
    try:
        payload = session.get(site, headers={'User-Agent': get_random_user_agent()}, verify=False, timeout=20, allow_redirects=True)
        
        if payload.status_code == 200:
            for cms, signs in CMS_SIGNS.items():
                if any(sign in payload.text for sign in signs):
                    print(f"[+] {cms} :: {site}")
                    with open(f'CMS/{cms}.txt', 'a') as file:
                        file.write(site + '\n')
                    return
            print(f"[+] UNKNOWN :: {site}")
            with open('CMS/Unknown.txt', 'a') as file:
                file.write(site + '\n')

        else:
            print(f"[+] UNKNOWN :: {site}")
            with open('CMS/Unknown.txt', 'a') as file:
                file.write(site + '\n')

    except Exception as e:
        print(f"[+] DEAD SITE :: {site}")
        with open('CMS/DeadSite.txt', 'a') as file:
            file.write(site + '\n')

def ensure_protocol(url):
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url
    return url

def process_urls(file_path, max_threads):
    if not os.path.exists('CMS'):
        os.makedirs('CMS')

    with open(file_path, 'r') as f:
        urls = f.readlines()

    with requests.Session() as session:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            executor.map(lambda site: check_cms(ensure_protocol(site.strip()), session), urls)

def main():
    file_path = input("Input List (ex: list.txt): ")
    max_threads = int(input("Input Thread: "))

    process_urls(file_path, max_threads)

if __name__ == "__main__":
    main()
