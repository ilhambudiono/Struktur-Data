# Simulasi Buku Telepon Sederhana
# Menggunakan List (Array Python)

class BukuTelepon:
    def __init__(self):
        self.kontak = []  # array untuk menyimpan data

    def tambah_kontak(self, nama, nomor):
        data = {"nama": nama, "nomor": nomor}
        self.kontak.append(data)
        print("Kontak berhasil ditambahkan!")

    def tampilkan_kontak(self):
        if not self.kontak:
            print("Buku telepon kosong.")
        else:
            print("\n=== DAFTAR KONTAK ===")
            for i, data in enumerate(self.kontak):
                print(f"{i+1}. {data['nama']} - {data['nomor']}")
            print("=====================")

    def cari_kontak(self, nama):
        ditemukan = False
        for data in self.kontak:
            if data["nama"].lower() == nama.lower():
                print(f"Kontak ditemukan: {data['nama']} - {data['nomor']}")
                ditemukan = True
        if not ditemukan:
            print("Kontak tidak ditemukan.")

    def hapus_kontak(self, nama):
        for data in self.kontak:
            if data["nama"].lower() == nama.lower():
                self.kontak.remove(data)
                print("Kontak berhasil dihapus.")
                return
        print("Kontak tidak ditemukan.")


def menu():
    buku = BukuTelepon()

    while True:
        print("\n=== MENU BUKU TELEPON ===")
        print("1. Tambah Kontak")
        print("2. Tampilkan Kontak")
        print("3. Cari Kontak")
        print("4. Hapus Kontak")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            nama = input("Masukkan nama: ")
            nomor = input("Masukkan nomor: ")
            buku.tambah_kontak(nama, nomor)

        elif pilihan == "2":
            buku.tampilkan_kontak()

        elif pilihan == "3":
            nama = input("Masukkan nama yang dicari: ")
            buku.cari_kontak(nama)

        elif pilihan == "4":
            nama = input("Masukkan nama yang ingin dihapus: ")
            buku.hapus_kontak(nama)

        elif pilihan == "5":
            print("Terima kasih.")
            break

        else:
            print("Pilihan tidak valid!")


if __name__ == "__main__":
    menu()