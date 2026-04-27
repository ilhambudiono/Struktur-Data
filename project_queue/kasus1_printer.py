"""
kasus1_printer.py — Antrian Printer Bersama
============================================
Skenario:
  Banyak user mengirim dokumen ke 1 printer.
  Printer hanya bisa cetak 1 dokumen pada satu waktu.
  Dokumen yang datang duluan, dicetak duluan (FIFO).

Operasi:
  enqueue() → user mengirim dokumen baru
  dequeue() → printer mulai cetak dokumen berikutnya
"""

from queue import Queue


class PrinterQueue:
    """Simulasi antrian printer bersama."""

    def __init__(self):
        self._queue = Queue(max_size=50)
        self._total_sent = 0
        self._total_printed = 0

    def kirim_dokumen(self, nama_file: str, pengirim: str = "User"):
        """User mengirim dokumen ke antrian printer."""
        self._queue.enqueue(nama_file)
        self._total_sent += 1
        print(f"  [KIRIM]  {pengirim} → '{nama_file}' ditambahkan ke antrian "
              f"(posisi ke-{len(self._queue)})")

    def cetak_berikutnya(self):
        """Printer memproses dokumen paling depan."""
        if self._queue.is_empty():
            print("  [INFO]   Tidak ada dokumen dalam antrian.")
            return None
        doc = self._queue.dequeue()
        self._total_printed += 1
        print(f"  [CETAK]  Mencetak: '{doc}'  "
              f"(sisa antrian: {len(self._queue)})")
        return doc

    def cetak_semua(self):
        """Printer memproses semua dokumen hingga antrian kosong."""
        print("  [START]  Printer mulai memproses antrian...")
        while not self._queue.is_empty():
            self.cetak_berikutnya()
        print("  [DONE]   Semua dokumen selesai dicetak.")

    def status(self):
        print(f"\n  Dokumen terkirim : {self._total_sent}")
        print(f"  Dokumen dicetak  : {self._total_printed}")
        print(f"  Dalam antrian    : {len(self._queue)}")
        print(f"  Antrian          : {self._queue}")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KASUS 1: Antrian Printer Bersama")
    print("=" * 55)

    printer = PrinterQueue()

    print("\n--- User mengirim dokumen ---")
    printer.kirim_dokumen("laporan.pdf",  pengirim="Andi")
    printer.kirim_dokumen("tugas.docx",   pengirim="Budi")
    printer.kirim_dokumen("foto.jpg",     pengirim="Citra")
    printer.kirim_dokumen("slide.pptx",   pengirim="Dedi")

    print("\n--- Cetak 1 dokumen ---")
    printer.cetak_berikutnya()

    print("\n--- Dokumen baru masuk saat printer sedang sibuk ---")
    printer.kirim_dokumen("invoice.pdf",  pengirim="Eka")

    print("\n--- Cetak semua sisa dokumen ---")
    printer.cetak_semua()

    print("\n--- Status Akhir ---")
    printer.status()
