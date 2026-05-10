"""
SOAL 2 - Doubly Linked List: Chronological & Alphabetical Views
================================================================
Satu koleksi note dengan DUA doubly linked list:
  - Chronological DLL : urut berdasarkan waktu dibuat (terbaru di depan)
  - Alphabetical DLL  : urut berdasarkan judul (A → Z)

Satu node fisik, dua logical chain → prinsip multi-linked.
"""

from __future__ import annotations
from datetime import datetime
from typing import Optional


# ─── Node ────────────────────────────────────────────────────────────────────

class NoteNode:
    """
    Satu note dengan DUA pasang pointer DLL:
      - (chrono_prev, chrono_next) → chain urutan waktu
      - (alpha_prev,  alpha_next)  → chain urutan alfabet
    """

    def __init__(self, note_id: int, title: str, content: str):
        self.note_id = note_id
        self.title   = title
        self.content = content
        self.created = datetime.now()

        # Doubly links – chronological chain
        self.chrono_prev: Optional[NoteNode] = None
        self.chrono_next: Optional[NoteNode] = None

        # Doubly links – alphabetical chain
        self.alpha_prev:  Optional[NoteNode] = None
        self.alpha_next:  Optional[NoteNode] = None

    def __repr__(self):
        ts = self.created.strftime("%H:%M:%S.%f")[:-3]
        return f"Note(id={self.note_id}, title='{self.title}', created={ts})"


# ─── Generic DLL Helper ───────────────────────────────────────────────────────

class DLL:
    """
    Doubly Linked List generik.
    prev/next field dipilih lewat string key ('chrono' atau 'alpha').
    """

    def __init__(self, key: str):
        self.key  = key          # 'chrono' atau 'alpha'
        self.head: Optional[NoteNode] = None
        self.tail: Optional[NoteNode] = None
        self.size = 0

    # ── Getter/Setter pointer helper ──────────────────────────────────────────

    def _prev(self, node: NoteNode) -> Optional[NoteNode]:
        return getattr(node, f"{self.key}_prev")

    def _next(self, node: NoteNode) -> Optional[NoteNode]:
        return getattr(node, f"{self.key}_next")

    def _set_prev(self, node: NoteNode, val: Optional[NoteNode]):
        setattr(node, f"{self.key}_prev", val)

    def _set_next(self, node: NoteNode, val: Optional[NoteNode]):
        setattr(node, f"{self.key}_next", val)

    # ── Insert ────────────────────────────────────────────────────────────────

    def insert_front(self, node: NoteNode) -> None:
        """Sisipkan node di depan (O(1))."""
        self._set_next(node, self.head)
        self._set_prev(node, None)
        if self.head:
            self._set_prev(self.head, node)
        self.head = node
        if self.tail is None:
            self.tail = node
        self.size += 1

    def insert_sorted_alpha(self, node: NoteNode) -> None:
        """Sisipkan node di posisi alfabet yang tepat (O(n))."""
        cur = self.head
        while cur and cur.title.lower() <= node.title.lower():
            cur = self._next(cur)

        if cur is None:                       # masuk di belakang
            self._set_prev(node, self.tail)
            self._set_next(node, None)
            if self.tail:
                self._set_next(self.tail, node)
            self.tail = node
            if self.head is None:
                self.head = node

        elif self._prev(cur) is None:         # masuk di depan
            self.insert_front(node)
            self.size -= 1                    # insert_front sudah +1, koreksi

        else:                                 # masuk di tengah
            prev_node = self._prev(cur)
            self._set_next(prev_node, node)
            self._set_prev(node, prev_node)
            self._set_next(node, cur)
            self._set_prev(cur, node)

        self.size += 1

    # ── Delete ────────────────────────────────────────────────────────────────

    def remove(self, node: NoteNode) -> None:
        """
        Hapus node dari chain ini (O(1) jika referensi node diketahui).
        Keunggulan DLL: tidak perlu tracking predecessor!
        """
        p = self._prev(node)
        n = self._next(node)

        if p:
            self._set_next(p, n)
        else:
            self.head = n              # node adalah head

        if n:
            self._set_prev(n, p)
        else:
            self.tail = p              # node adalah tail

        self._set_prev(node, None)
        self._set_next(node, None)
        self.size -= 1

    # ── Traversal ─────────────────────────────────────────────────────────────

    def forward(self) -> list[NoteNode]:
        result, cur = [], self.head
        while cur:
            result.append(cur)
            cur = self._next(cur)
        return result

    def backward(self) -> list[NoteNode]:
        """Traversal terbalik – O(n), keunggulan DLL vs SLL."""
        result, cur = [], self.tail
        while cur:
            result.append(cur)
            cur = self._prev(cur)
        return result


# ─── NoteStore ────────────────────────────────────────────────────────────────

class NoteStore:
    """
    Mengelola dua view DLL (chronological & alphabetical) untuk satu set note.
    """

    def __init__(self):
        self._notes:   dict[int, NoteNode] = {}
        self.chrono    = DLL("chrono")   # terbaru di depan
        self.alpha     = DLL("alpha")    # A → Z
        self._next_id  = 1

    def add_note(self, title: str, content: str) -> NoteNode:
        """
        Tambah note → masuk ke KEDUA chain.
        O(n) total (O(1) chrono + O(n) alpha sort).
        """
        node = NoteNode(self._next_id, title, content)
        self._next_id += 1
        self._notes[node.note_id] = node

        self.chrono.insert_front(node)        # terbaru di depan
        self.alpha.insert_sorted_alpha(node)  # sesuai alfabet

        return node

    def delete_note(self, note_id: int) -> None:
        """
        Hapus note dari KEDUA chain – wajib untuk menjaga konsistensi!
        """
        node = self._notes.pop(note_id, None)
        if node is None:
            print(f"Note id={note_id} tidak ditemukan.")
            return
        self.chrono.remove(node)
        self.alpha.remove(node)

    def view_chronological(self) -> list[NoteNode]:
        return self.chrono.forward()

    def view_chronological_reverse(self) -> list[NoteNode]:
        """Lihat note dari yang tertua – O(n) berkat DLL."""
        return self.chrono.backward()

    def view_alphabetical(self) -> list[NoteNode]:
        return self.alpha.forward()


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import time

    store = NoteStore()

    n1 = store.add_note("Zeta Note",   "isi z"); time.sleep(0.01)
    n2 = store.add_note("Alpha Note",  "isi a"); time.sleep(0.01)
    n3 = store.add_note("Mango Note",  "isi m"); time.sleep(0.01)
    n4 = store.add_note("Beta Note",   "isi b"); time.sleep(0.01)
    n5 = store.add_note("Cherry Note", "isi c")

    print("=== Chronological View (terbaru → terlama) ===")
    for n in store.view_chronological():
        print(" ", n)

    print("\n=== Chronological Reverse (terlama → terbaru) ===")
    for n in store.view_chronological_reverse():
        print(" ", n)

    print("\n=== Alphabetical View (A → Z) ===")
    for n in store.view_alphabetical():
        print(" ", n)

    print(f"\n--- Hapus '{n3.title}' (id={n3.note_id}) ---")
    store.delete_note(n3.note_id)

    print("=== Chronological setelah delete ===")
    for n in store.view_chronological():
        print(" ", n)

    print("=== Alphabetical setelah delete ===")
    for n in store.view_alphabetical():
        print(" ", n)
