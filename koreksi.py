import numpy as np
from collections import defaultdict

# Fungsi untuk membangun bigram dari sebuah kata
def createBigram(word):
    return [word[i:i+2] for i in range(len(word) - 1)]

# Fungsi untuk menghitung cosine similarity
def cosineSimilarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)  
    norm1 = np.linalg.norm(vec1)     
    norm2 = np.linalg.norm(vec2)
    if((norm1 * norm2)   != 0): 
        return dot_product / (norm1 * norm2)  
    else:
        return 0

# Fungsi untuk memproses query dan menghitung vektor bigram
def createVektorQuery(query, bigramIdx):
    # membangun bigram kata 
    query_bigrams = createBigram(query)
    
    # menghitung jumlah kemunculan bigram
    bigram_counts = defaultdict(int)
    for bigram in query_bigrams:
        bigram_counts[bigram] += 1
    
    # membuat vektor kata
    vektorQuery = np.zeros(len(bigramIdx), dtype=int)
    for bigram, count in bigram_counts.items():
        if bigram in bigramIdx:
            vektorQuery[bigramIdx[bigram]] = count
        else:
            print(f"PERINGATAN: Bigram '{bigram}' tidak ditemukan pada bigramIdx")
    return vektorQuery

# Fungsi untuk menghitung panjang kata sebagai bobot
def lengthWeight(query, word):
    len_query = len(query)
    len_word = len(word)
    
    # Jika panjang kata dalam rentang len_query-1, len_query, atau len_query+1
    if abs(len_query - len_word) <= 2:
        return 1  # Bobot yang sama jika panjang kata sama atau hanya berbeda 1
    else:
        return 0.5  # Bobot 0.5 jika panjang kata lebih dari 1 karakter berbeda

# Fungsi untuk membangun vektor bigram dari dataset
def createVektorKata(dataset):
    word_bigrams = {}
    allBigram = set()  # Untuk menyimpan semua bigram unik
    
    for word in dataset:
        bigrams = createBigram(word)
        word_bigrams[word] = bigrams
        allBigram.update(bigrams)  # Menambah bigram unik ke set
        
    # Mengonversi bigram unik ke list untuk digunakan dalam vektor
    allBigram = sorted(list(allBigram))
    bigramIdx = {bigram: idx for idx, bigram in enumerate(allBigram)}

    # Membuat vektor bigram untuk setiap kata
    vektorDataset = {}
    for word, bigrams in word_bigrams.items():
        vector = np.zeros(len(allBigram), dtype=int)
        for bigram in bigrams:
            if bigram in bigramIdx:
                vector[bigramIdx[bigram]] += 1
        vektorDataset[word] = vector
    return vektorDataset, bigramIdx

# Fungsi untuk mencari 5 koreksi terbaik
def koreksiKata(query, vektorDataset, bigramIdx):
    vektorQuery = createVektorQuery(query, bigramIdx)
    similarities = []
    for word, word_vector in vektorDataset.items():
        # Menghitung cosine similarity
        similarity = cosineSimilarity(vektorQuery, word_vector)
        # Menghitung bobot panjang kata
        length_factor = lengthWeight(query, word)
        # Menggabungkan cosine similarity dan bobot panjang kata
        weighted_similarity = similarity * length_factor
        similarities.append((word, weighted_similarity))
    # Mengurutkan berdasarkan similarity dan mengambil 5 hasil teratas
    similarities.sort(key=lambda x: x[1], reverse=True)
    return similarities[:5]