from utility import *
import sys, os

def art():
    print("""    
┳┓       ┓   ┏┓          ┓
┣┫┏┓┏┓┏┓┏┣┓  ┃┃┏┓┏┓╋┏┓┏┏┓┃
┻┛┛ ┗ ┗┻┗┛┗  ┣┛┛ ┗┛┗┗┛┗┗┛┗ 
          
Welcome to Breach Protocol Solver!      
""")
def print_menu():
    print("""
Menu:
[1] berkas .txt
[2] CLI input (Auto Generate)
          
[E] Exit
    """)

def main():
    base_dir = os.path.dirname(__file__) 
    test_dir = os.path.join(base_dir, '..', 'test')

    while True:
        art()
        print_menu()
        command = input("Masukkan pilihan Anda: ")
        
        if command == '1':
            file_name = input("\nMasukkan nama berkas/file ber-ekstensi .txt: ")
            file_path = os.path.join(test_dir, file_name)
            
            if os.path.isfile(file_path):
                buffer_size, matrix, sequences = input_file(file_path)
                print("\nTunggu sebentar, program sedang mencari solusi ...\n")
                generate_valid_paths(matrix, buffer_size, sequences, file_path)
            else:
                print(f"\nFile '{file_path}' tidak ditemukan. Silakan coba lagi.")
        elif command == '2':
            buffer_size, matrix, sequences = generate_game_data()
            print_game_data(buffer_size, matrix, sequences)
            print("\nTunggu sebentar, program sedang mencari solusi ...\n")
            generate_valid_paths(matrix, buffer_size, sequences)
        elif command.lower() == 'e':
            print("\nKeluar dari program...\n")
            sys.exit()
        else:
            print("\nPilihan tidak valid, silakan coba lagi.\n")


if __name__ == "__main__":
    main()