import socket


input_file = input("(contoh: domains.txt): ").strip()

try:
    with open(input_file, "r") as f:
        domains = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"❌ File '{input_file}' tidak ditemukan.")
    exit(1)

ip_set = set()

for domain in domains:
    try:
        ip = socket.gethostbyname(domain)
        ip_set.add(ip)
        print(f"{domain} => {ip}")
    except socket.gaierror:
        print(f"[!] Gagal resolve: {domain}")

# Simpan hasil IP unik ke file
output_file = "ips.txt"
with open(output_file, "w") as f:
    for ip in sorted(ip_set):
        f.write(ip + "\n")

print(f"\n✅ Total IP unik: {len(ip_set)}")
print(f"📄 Hasil disimpan ke: {output_file}")
