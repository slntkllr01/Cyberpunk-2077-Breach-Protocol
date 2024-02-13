import random
import time
import os

# Fungsi untuk menghasilkan jalur valid dari matriks sesuai dengan buffer size dan sekuen yang diberikan
def generate_valid_paths(matrix, buffer_size, sequences, input_file_name=None):
    # Catat waktu mulai eksekusi
    start_time = time.time()

    # Inisialisasi ukuran matriks dan array
    rows = len(matrix)
    cols = len(matrix[0])
    unique_paths = []
    results = []

    # Iterasi melalui setiap kolom di baris pertama untuk menentukan titik awal
    for start_col in range(cols):
        # Setiap titik awal dijadikan sebagai jalur awal
        paths = [[(0, start_col)]]

        # Ekspansi jalur
        while paths:
            new_paths = []
            for path in paths:
                path_tuple = tuple(path)
                # Jika jalur tidak melebihi buffer size dan belum ada sebelumnya
                if len(path) <= buffer_size and path_tuple not in unique_paths:
                    unique_paths.append(path_tuple)
                    results.append(path)

                # Jika jalur sudah mencapai buffer size, lanjutkan ke jalur berikutnya
                if len(path) == buffer_size:
                    continue
                
                # Tambahkan langkah baru ke jalur berdasarkan aturan pergerakan (Vertikal - Horizontal)
                last_r, last_c = path[len(path)-1]
                if len(path) % 2 == 1: # Pergerakan vertikal
                    for r in range(rows):
                        if (r, last_c) not in path:
                            new_path = path + [(r, last_c)]
                            new_paths.append(new_path)
                else: # Pergerakan horizontal
                    for c in range(cols):
                        if (last_r, c) not in path:
                            new_path = path + [(last_r, c)]
                            new_paths.append(new_path)
            paths = new_paths

    # Konversi jalur menjadi sekuen matriks
    final_results = [[matrix[r][c] for r, c in path] for path in results]

    # Fungsi untuk mengecek apakah jalur merupakan subsekuen dari sekuen yang diberikan
    def is_subsequence(path, sequence):
        seq_index = 0 
        for item in path:
            if item == sequence[seq_index]:
                seq_index += 1 
                if seq_index == len(sequence): 
                    return True
            else:
                if seq_index > 0:
                    seq_index = 0
                    if item == sequence[seq_index]:
                        seq_index += 1
        return False

    # Fungsi untuk menghitung total bobot dari jalur berdasarkan sekuen yang ditemukan
    def calculate_weight(path, sequences):
        total_weight = 0
        for i in range(len(sequences)):
            seq = sequences[i][0] 
            weight = sequences[i][1]
            if is_subsequence(path, seq):
                total_weight += weight
        return total_weight

    # Menemukan jalur yang menghasilkan bobot maksimum
    max_weight = 0
    max_weight_solutions = []
    for i in range(len(final_results)):
        path = final_results[i]
        weight = calculate_weight(path, sequences)
        if weight > max_weight:
            max_weight = weight
            max_weight_solutions = [(path, weight)]
        elif weight == max_weight:
            max_weight_solutions.append((path, weight))

    # Hitung waktu eksekusi
    execution_time = (time.time() - start_time) * 1000  # Waktu eksekusi

    # Siapkan output
    output = ""
    if not max_weight_solutions or (max_weight_solutions and max_weight_solutions[0][1] == 0):
        output += "Maaf, tidak ada sekuen yang berhasil didapatkan.\n\n"
    else:
        max_weight = max_weight_solutions[0][1]
        output += f"{max_weight}\n"
        for path, weight in max_weight_solutions:
            if weight == max_weight: 
                output += ' '.join(path) + "\n"
                for r, c in results[final_results.index(path)]:
                    output += f"{c + 1}, {r + 1}\n"
                break  
    
    output += f"\n{execution_time:.2f} ms\n"
    
    # Mencetak output ke terminal
    print(output)

    # Tawarkan pengguna untuk menyimpan solusi
    save_prompt = input("Apakah ingin menyimpan solusi? (y/n): ")
    if save_prompt.lower() == 'y':
        save_solution(output, input_file_name)

# Fungsi untuk menyimpan solusi ke dalam berkas
def save_solution(output, input_file_name=None):
    # Menentukan direktori tempat menyimpan file solusi
    base_dir = os.path.dirname(__file__) 
    solution_dir = os.path.join(base_dir, '..', 'test')

    if input_file_name:
        # Jika nama file input diberikan, buat nama file solusi berdasarkan format yang saya buat (_solution.txt)
        base_name = os.path.splitext(os.path.basename(input_file_name))[0]
        file_name = os.path.join(solution_dir, f"{base_name}_solution.txt")
    else:
        # Jika tidak, minta pengguna memasukkan nama file
        file_name_input = input("Masukkan nama berkas (tanpa ekstensi .txt): ")
        file_name = os.path.join(solution_dir, f"{file_name_input}.txt")

    with open(file_name, 'w') as file:
        file.write(output)
    print(f"\nSolusi telah disimpan dalam berkas '{file_name}'.")

# Fungsi untuk menghasilkan data permainan secara otomatis dari input pengguna
def generate_game_data():
    num_unique_tokens = int(input("\nMasukkan Jumlah Token Unik: "))
    tokens_input = input("Masukkan Daftar Token yang Anda Inginkan (Pisahkan dengan Spasi): ")
    tokens = tokens_input.split()
    buffer_size = int(input("Masukkan Ukuran Buffer: "))
    matrix_size = input("Masukkan Ukuran Matriks (format: lebarxtinggi): ")
    num_sequences = int(input("Masukkan Jumlah Sekuens: "))
    max_sequence_size = int(input("Masukkan Ukuran Maksimal Sekuens: "))
    matrix_width, matrix_height = map(int, matrix_size.split())
    
    matrix = [[random.choice(tokens) for _ in range(matrix_width)] for _ in range(matrix_height)]
    
    sequences = []
    for _ in range(num_sequences):
        sequence_length = random.randint(1, max_sequence_size)
        sequence = [random.choice(tokens) for _ in range(sequence_length)]
        reward = random.randint(1, 100)
        sequences.append((sequence, reward))
    
    return buffer_size, matrix, sequences

# Fungsi untuk mencetak data permainan yang dihasilkan
def print_game_data(buffer_size, matrix, sequences):
    print("\nMatriks dan Sekuens Permainan berhasil dibuat!")
    print(f"\nBuffer Size: {buffer_size}\n")
    for row in matrix:
        print(' '.join(row))
    print("\nSekuens beserta hadiah yang dapat diperoleh:")
    for i, (sequence, reward) in enumerate(sequences, start=1):
        print(f"{i}. {' '.join(sequence)} dengan Bobot Hadiah {reward}")

# Fungsi untuk membaca data permainan dari berkas
def input_file(file_name):
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, '..', 'test', file_name)

    with open(file_path, 'r') as file:
        buffer_size = int(file.readline().strip())
        matrix_width, matrix_height = map(int, file.readline().strip().split())
        
        matrix = []
        for _ in range(matrix_height):
            row = file.readline().strip().split()
            matrix.append(row)
        
        number_of_sequences = int(file.readline().strip())
        sequences = []
        for _ in range(number_of_sequences):
            sequence = file.readline().strip().split()
            reward = int(file.readline().strip())
            sequences.append((sequence, reward))
        
    return buffer_size, matrix, sequences