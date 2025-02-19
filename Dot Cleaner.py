def filter_urls(url_list):
    # Hanya mempertahankan URL yang tidak mengandung '...'
    return [url for url in url_list if '...' not in url]

def read_urls_from_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.strip() for line in file.readlines()]
    except FileNotFoundError:
        print(f"File {file_name} tidak ditemukan.")
        return []

def write_urls_to_file(file_name, url_list):
    with open(file_name, 'w') as file:
        for url in url_list:
            file.write(url + '\n')

# Meminta input nama file dari pengguna
file_name = input("Masukkan nama file teks yang berisi daftar URL: ")

# Membaca URL dari file
urls = read_urls_from_file(file_name)

if urls:
    # Memanggil fungsi untuk memfilter URL
    filtered_urls = filter_urls(urls)

    # Menulis URL yang telah difilter kembali ke file yang sama
    write_urls_to_file(file_name, filtered_urls)

    print("\nDaftar URL telah difilter dan ditulis kembali ke file.")
else:
    print("Tidak ada URL yang dapat diproses.")
