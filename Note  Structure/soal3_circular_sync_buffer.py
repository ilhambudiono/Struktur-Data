"""
SOAL 3 - Circular Linked List: Sync Status Buffer
===================================================
Circular buffer untuk melacak perubahan terbaru (recent changes).
Digunakan untuk fitur "sync status tracking" pada aplikasi note-taking.

Cara kerja:
  - Buffer berkapasitas N (default 5 perubahan terakhir).
  - Saat buffer penuh, entry terlama ditimpa (overwrite / round-robin).
  - listRef menunjuk ke NODE TERAKHIR yang ditulis (entry terbaru).
  - listRef.next → entry tertua (yang akan ditimpa berikutnya).
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional
from enum import Enum


# ─── Model ───────────────────────────────────────────────────────────────────

class SyncStatus(Enum):
    PENDING   = "PENDING"    # belum disinkron
    SYNCED    = "SYNCED"     # berhasil sync
    FAILED    = "FAILED"     # sync gagal
    CONFLICT  = "CONFLICT"   # konflik dengan server


class ChangeRecord:
    """Satu entry perubahan yang dicatat di buffer."""

    def __init__(self, note_id: int, action: str, status: SyncStatus):
        self.note_id   = note_id
        self.action    = action          # "ADD", "EDIT", "DELETE"
        self.status    = status
        self.timestamp = datetime.now()

    def __repr__(self):
        ts = self.timestamp.strftime("%H:%M:%S.%f")[:-3]
        return (f"Change(note={self.note_id}, action={self.action}, "
                f"status={self.status.value}, ts={ts})")


# ─── Circular Node ────────────────────────────────────────────────────────────

class CircularNode:
    """Node dalam circular linked list."""

    def __init__(self):
        self.record: Optional[ChangeRecord] = None   # None = slot kosong
        self.next:   Optional[CircularNode] = None


# ─── Circular Sync Buffer ─────────────────────────────────────────────────────

class SyncBuffer:
    """
    Circular linked list berkapasitas tetap (N node).
    Implementasi sesuai slide: listRef → NODE TERAKHIR.
    listRef.next → NODE PERTAMA / tertua (akan ditimpa berikutnya).

    Operasi utama:
      - push(record)    : tambah perubahan baru, O(1)
      - get_recent(k)   : ambil k perubahan terbaru, O(k)
      - update_status() : perbarui status entry tertentu, O(N)
    """

    def __init__(self, capacity: int = 5):
        if capacity < 1:
            raise ValueError("Capacity minimal 1.")
        self._capacity = capacity
        self._count    = 0       # jumlah slot terisi

        # Buat N node yang saling terhubung membentuk lingkaran
        first = CircularNode()
        prev  = first
        for _ in range(capacity - 1):
            node      = CircularNode()
            prev.next = node
            prev      = node
        prev.next = first          # tutup lingkaran

        # listRef → node terakhir (sebelum first = "write head" berikutnya)
        self._listRef: CircularNode = prev

    # ── Core Properties ───────────────────────────────────────────────────────

    @property
    def _write_head(self) -> CircularNode:
        """Node yang akan ditimpa pada push berikutnya (listRef.next)."""
        return self._listRef.next

    @property
    def is_empty(self) -> bool:
        return self._count == 0

    @property
    def is_full(self) -> bool:
        return self._count == self._capacity

    # ── Push ──────────────────────────────────────────────────────────────────

    def push(self, record: ChangeRecord) -> None:
        """
        Tulis record ke write_head, lalu majukan listRef.
        Jika penuh, write_head menimpa entry tertua (round-robin).
        O(1) – keunggulan circular list!
        """
        self._write_head.record = record

        # Majukan listRef ke write_head yang baru saja ditulis
        self._listRef = self._write_head

        if not self.is_full:
            self._count += 1

    # ── Read ──────────────────────────────────────────────────────────────────

    def get_recent(self, k: Optional[int] = None) -> list[ChangeRecord]:
        """
        Ambil k entry terbaru (default: semua terisi).
        Traversal dimulai dari listRef (terbaru) mundur lewat circular wrap.
        O(k).
        """
        if self.is_empty:
            return []
        k = min(k or self._count, self._count)

        result = []
        # Kumpulkan semua node terisi dalam urutan terbaru → terlama
        # listRef = terbaru; mundur dengan menghitung N langkah
        nodes = []
        cur = self._listRef
        for _ in range(self._count):
            if cur.record is not None:
                nodes.append(cur)
            # mundur: dalam singly circular kita maju dulu sampai "satu sebelum cur"
            # Trik: simpan semua dulu, balik urutannya
            cur = cur.next   # akan di-reverse di bawah

        # Traversal ke depan menghasilkan urutan tertua → terbaru,
        # kita collect dari write_head.next (= slot tertua terisi)
        ordered = self._collect_oldest_first()
        return [n.record for n in ordered[-k:]][::-1]

    def _collect_oldest_first(self) -> list[CircularNode]:
        """
        Kumpulkan semua node terisi mulai dari yang tertua.
        Tertua = write_head (akan ditimpa berikutnya).
        """
        result = []
        cur    = self._write_head        # slot tertua (atau kosong pertama)
        done   = False
        # Traversal circular: berhenti setelah kembali ke write_head
        # Gunakan counter karena tidak ada NULL terminator
        for _ in range(self._capacity):
            if cur.record is not None:
                result.append(cur)
            cur = cur.next
        return result

    def get_all(self) -> list[ChangeRecord]:
        """Semua record dari terlama ke terbaru."""
        return [n.record for n in self._collect_oldest_first()]

    # ── Update Status ─────────────────────────────────────────────────────────

    def update_status(self, note_id: int, new_status: SyncStatus) -> int:
        """
        Perbarui status semua entry untuk note_id tertentu.
        O(N) di mana N = kapasitas buffer.
        Mengembalikan jumlah entry yang diperbarui.
        """
        updated = 0
        cur     = self._listRef
        for _ in range(self._capacity):
            cur = cur.next
            if cur.record and cur.record.note_id == note_id:
                cur.record.status = new_status
                updated += 1
        return updated

    # ── Display ───────────────────────────────────────────────────────────────

    def display(self) -> None:
        all_records = self.get_all()
        print(f"SyncBuffer [{self._count}/{self._capacity}]")
        if not all_records:
            print("  (kosong)")
            return
        for i, rec in enumerate(reversed(all_records), 1):
            marker = " ← TERBARU" if i == 1 else ""
            print(f"  [{i}] {rec}{marker}")


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import time

    buf = SyncBuffer(capacity=4)   # buffer untuk 4 perubahan terakhir

    print("=== Tambah 3 perubahan (buffer belum penuh) ===")
    buf.push(ChangeRecord(note_id=1, action="ADD",  status=SyncStatus.PENDING))
    time.sleep(0.01)
    buf.push(ChangeRecord(note_id=2, action="EDIT", status=SyncStatus.SYNCED))
    time.sleep(0.01)
    buf.push(ChangeRecord(note_id=1, action="EDIT", status=SyncStatus.PENDING))
    buf.display()

    print("\n=== Tambah 2 lagi (buffer jadi penuh, lalu overwrite entry tertua) ===")
    time.sleep(0.01)
    buf.push(ChangeRecord(note_id=3, action="DELETE", status=SyncStatus.FAILED))
    time.sleep(0.01)
    buf.push(ChangeRecord(note_id=4, action="ADD",    status=SyncStatus.PENDING))
    buf.display()

    print("\n=== Tambah 1 lagi (overwrite entry tertua karena sudah penuh) ===")
    time.sleep(0.01)
    buf.push(ChangeRecord(note_id=5, action="EDIT", status=SyncStatus.CONFLICT))
    buf.display()

    print("\n=== 2 perubahan terbaru ===")
    for r in buf.get_recent(2):
        print(" ", r)

    print("\n=== Update status note_id=1 → SYNCED ===")
    n = buf.update_status(note_id=1, new_status=SyncStatus.SYNCED)
    print(f"  {n} entry diperbarui")
    buf.display()
