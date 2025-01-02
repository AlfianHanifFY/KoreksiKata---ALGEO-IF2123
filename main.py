

from koreksi import *
import time

# Menyiapkan dataset
with open("data.txt", "r") as file:
    dataset = file.read().splitlines()

# Membangun vektor bigram untuk dataset
startTime = time.time()
vektorDataset, allBigram = createVektorKata(dataset)
print(f"\n\033[1;32mVektor kata selesai dibangun dalam {time.time() - startTime:.2f} detik.\033[0m")
# Loop untuk input query
while True:
    query = input("\n\033[1;34mMasukkan Kata (atau '\033[1;31mexit\033[1;34m' untuk keluar): \033[0m").strip()
    if query.lower() == 'exit':
        print("\033[1;31mProgram selesai.\033[0m")
        break

    if not query:
        print("\033[1;31mInput tidak boleh kosong.\033[0m")
        continue

    # Mencari 5 koreksi terbaik
    startTime = time.time()
    topKoreksi = koreksiKata(query, vektorDataset, allBigram)
    elapsedTime = time.time() - startTime

    # Menampilkan hasil dalam bentuk tabel sederhana
    if topKoreksi:
        print("\n\033[1;33mTop 5 Kata:\033[0m")
        print("+----+----------------+-------------------+")
        print("| No | Koreksi        | Skor Similarity   |")
        print("+----+----------------+-------------------+")
        for i, (word, similarity) in enumerate(topKoreksi, start=1):
            print(f"| {i:<2} | {word:<14} | {similarity:<17.4f} |")
        print("+----+----------------+-------------------+")
    else:
        print("\033[1;31mTidak ada koreksi yang ditemukan.\033[0m")

    print(f"\n\033[1;32mWaktu yang dibutuhkan: {elapsedTime:.4f} detik\033[0m")




