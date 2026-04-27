"""
kasus3_antrian_rs.py — Antrian Rumah Sakit (Priority Queue)
============================================================
Skenario:
  Pasien datang dengan tingkat urgensi berbeda.
  Pasien kritis didahulukan, bukan murni FIFO.
  Prioritas sama → urutan kedatangan tetap dipakai (FIFO).

Level prioritas:
  0 = Kritis   (merah)
  1 = Darurat  (oranye)
  2 = Menengah (kuning)
  3 = Ringan   (hijau)

Implementasi:
  BoundedPriorityQueue — satu Queue per level prioritas.
  dequeue() selalu mengambil dari level terendah yang tidak kosong.
"""

from queue import Queue


LABEL_PRIORITAS = {0: "Kritis", 1: "Darurat", 2: "Menengah", 3: "Ringan"}


class BoundedPriorityQueue:
    """
    Priority Queue dengan jumlah level tetap.
    Tiap level diimplementasikan sebagai Queue terpisah.
    enqueue: O(1) | dequeue: O(k) di mana k = jumlah level (tetap kecil)
    """

    def __init__(self, levels: int = 4, capacity_per_level: int = 50):
        self._levels = levels
        self._queues = [Queue(max_size=capacity_per_level) for _ in range(levels)]

    def is_empty(self) -> bool:
        return all(q.is_empty() for q in self._queues)

    def __len__(self) -> int:
        return sum(len(q) for q in self._queues)

    def enqueue(self, item, priority: int):
        """Tambah item ke antrian sesuai level prioritasnya."""
        assert 0 <= priority < self._levels, (
            f"Prioritas harus 0–{self._levels - 1}"
        )
        self._queues[priority].enqueue(item)

    def dequeue(self):
        """Ambil item dari level prioritas tertinggi (angka terkecil)."""
        for q in self._queues:
            if not q.is_empty():
                return q.dequeue()
        raise AssertionError("Priority Queue kosong!")

    def peek(self):
        for q in self._queues:
            if not q.is_empty():
                return q.peek()
        raise AssertionError("Priority Queue kosong!")

    def tampilkan_antrian(self):
        """Tampilkan isi semua level antrian."""
        for i, q in enumerate(self._queues):
            if not q.is_empty():
                items = []
                for j in range(len(q)):
                    item = q.dequeue()
                    items.append(item)
                    q.enqueue(item)
                label = LABEL_PRIORITAS.get(i, str(i))
                print(f"    [{i}] {label:<10}: {items}")


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KASUS 3: Antrian Rumah Sakit (Priority Queue)")
    print("=" * 55)

    pq = BoundedPriorityQueue(levels=4)

    print("\n--- Pasien berdatangan ---")
    pasien = [
        ("Budi",  3), ("Ani",   0), ("Citra", 2),
        ("Dedi",  0), ("Eka",   1), ("Fani",  2),
        ("Gita",  1), ("Hadi",  3),
    ]
    for nama, prio in pasien:
        pq.enqueue(nama, prio)
        print(f"  [DAFTAR] {nama:<8} — {LABEL_PRIORITAS[prio]}")

    print(f"\n  Total pasien menunggu : {len(pq)}")
    print("\n--- Isi antrian per level ---")
    pq.tampilkan_antrian()

    print("\n--- Proses layanan ---")
    urutan = []
    while not pq.is_empty():
        pasien_dilayani = pq.dequeue()
        urutan.append(pasien_dilayani)
        print(f"  [LAYANI] {pasien_dilayani}")

    print(f"\n  Urutan layanan : {urutan}")
    print("\n  Catatan: Ani & Dedi sama-sama Kritis (pr=0),")
    print("  Ani datang duluan → dilayani duluan (FIFO dalam prioritas).")
