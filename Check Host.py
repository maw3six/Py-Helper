import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import os

requests.packages.urllib3.disable_warnings()

BANNER = r"""
 ██████╗███████╗██╗  ██╗███████╗██████╗ ██████╗ ██╗   ██╗
██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝
██║     █████╗  █████╔╝ █████╗  ██████╔╝██████╔╝ ╚████╔╝ 
██║     ██╔══╝  ██╔═██╗ ██╔══╝  ██╔══██╗██╔═══╝   ╚██╔╝  
╚██████╗███████╗██║  ██╗███████╗██║  ██║██║        ██║   
 ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝        ╚═╝                     
	Created by: @maw3six
"""

def check_domain_status(domain):
    try:
        response = requests.get(f"http://{domain}", timeout=5, verify=False)
        if response.status_code == 200:
            return domain, "Hidup"
        else:
            return domain, f"Mati (Status: {response.status_code})"
    except requests.RequestException:
        return domain, "Mati (Timeout atau Error)"


def main():
    print(BANNER)
    print("Checker Host Hidup Atau Modar!!\n")
    file_name = input("Daftar Url (misal: list.txt): ")

    try:
        with open(file_name, "r") as domain_file:
            domains = [line.strip() for line in domain_file if line.strip()]
    except FileNotFoundError:
        print(f"File {file_name} tidak ditemukan.")
        return

    print(f"Memulai pengecekan {len(domains)} domain...\n")

    file_base_name = os.path.splitext(file_name)[0]
    hidup_file_name = f"{file_base_name}-hidup.txt"
    mati_file_name = f"{file_base_name}-modar.txt"

    with open(hidup_file_name, "a") as hidup_file, open(mati_file_name, "a") as mati_file:
        with ThreadPoolExecutor(max_workers=20) as executor:
            future_to_domain = {executor.submit(check_domain_status, domain): domain for domain in domains}

            for future in tqdm(as_completed(future_to_domain), total=len(domains), desc="Memeriksa domain"):
                domain, status = future.result()
                if status == "Hidup":
                    hidup_file.write(f"{domain}\n")
                    print(f"{domain} [✓] Hidup")
                else:
                    mati_file.write(f"{domain} - {status}\n")
                    print(f"{domain} [✗] {status}")

    print(f"\nProses selesai. Hasil disimpan dalam file '{hidup_file_name}' dan '{mati_file_name}'.")


if __name__ == "__main__":
    main()
