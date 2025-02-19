import os

def combine_files_in_folder(folder_path):
    # Set untuk menyimpan URL unik (untuk menghindari duplikat)
    unique_lines = set()

    # Menelusuri semua file di dalam folder
    for file_name in os.listdir(folder_path):
        # Memeriksa apakah file berformat .txt
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)

            # Membaca file dan menambahkan isinya ke set (untuk menghindari duplikat)
            with open(file_path, 'r') as file:
                for line in file:
                    unique_lines.add(line.strip())

    return unique_lines

def write_combined_file(output_file, combined_data):
    with open(output_file, 'w') as file:
        for line in combined_data:
            file.write(line + '\n')

# Meminta input folder tempat file-file .txt berada
folder_path = input("Masukkan path folder yang berisi file .txt: ")

# Menggabungkan semua file .txt di dalam folder
combined_data = combine_files_in_folder(folder_path)

# Menulis data gabungan ke file baru
output_file = os.path.join(folder_path, 'combined_output.txt')
write_combined_file(output_file, combined_data)

print(f"\nSemua file telah digabungkan dan disimpan di {output_file}. Duplikat telah dihapus.")
