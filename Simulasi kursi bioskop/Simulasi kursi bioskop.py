# Hash Table Sederhana - Linear Probing
# Tema: Bioskop dan Kursi Penonton

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        # Menggunakan hash bawaan Python
        return hash(key) % self.size

    def insert(self, key):
        index = self.hash_function(key)
        start_index = index
        probes = 0

        print(f"\nPenonton '{key}' datang.")
        print(f"Nomor kursi awal (hash) = {index}")

        # Linear Probing
        while self.table[index] is not None:
            print(f"Kursi {index} sudah terisi oleh '{self.table[index]}' → Collision!")
            probes += 1
            index = (index + 1) % self.size
            print(f"Mencari kursi berikutnya → {index}")

            # Jika kembali ke posisi awal
            if index == start_index:
                print("Semua kursi penuh!")
                return

        self.table[index] = key
        print(f"Penonton '{key}' duduk di kursi {index}")
        print(f"Total probing: {probes}")

    def display(self):
        print("\n=== Daftar Kursi Bioskop ===")
        for i in range(self.size):
            print(f"Kursi {i} : {self.table[i]}")
        print("============================")

    def load_factor(self):
        filled = sum(1 for seat in self.table if seat is not None)
        return filled / self.size


# ===== Program Utama =====
if __name__ == "__main__":
    size = 10  # jumlah kursi
    bioskop = HashTable(size)

    penonton_list = ["Andi", "Budi", "Citra", "Dina", "Eko"]

    for penonton in penonton_list:
        bioskop.insert(penonton)

    bioskop.display()

    print(f"\nLoad Factor: {bioskop.load_factor():.2f}")