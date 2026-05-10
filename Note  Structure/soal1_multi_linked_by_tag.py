"""
SOAL 1 - Multi-Linked List: Multiple Tags per Note
===================================================
Setiap note bisa memiliki beberapa tag.
Setiap tag membentuk chain tersendiri.
Contoh: tag "python" punya chain semua note bertag python.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime


# ─── Node ────────────────────────────────────────────────────────────────────

class NoteNode:
    """
    Satu node = satu note.
    Setiap note bisa masuk ke banyak tag-chain sekaligus.
    Kunci multi-linked: tag_links menyimpan pointer 'next' untuk tiap tag.
    """

    def __init__(self, note_id: int, title: str, content: str, tags: list[str]):
        self.note_id  = note_id
        self.title    = title
        self.content  = content
        self.tags     = tags
        self.created  = datetime.now()

        # Multi-linked: satu entry per tag
        # tag_links["python"] = NoteNode berikutnya dalam chain tag "python"
        self.tag_links: dict[str, Optional[NoteNode]] = {t: None for t in tags}

    def __repr__(self):
        return f"NoteNode(id={self.note_id}, title='{self.title}', tags={self.tags})"


# ─── Tag Chain Manager ────────────────────────────────────────────────────────

class TagChain:
    """
    Satu chain untuk satu tag.
    head → node pertama yang memiliki tag ini.
    """

    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.head: Optional[NoteNode] = None
        self.size = 0

    def insert(self, new_node: NoteNode) -> None:
        """Sisipkan note ke depan chain tag ini (O(1))."""
        new_node.tag_links[self.tag_name] = self.head
        self.head = new_node
        self.size += 1

    def remove(self, target: NoteNode) -> None:
        """Hapus note dari chain tag ini (O(n))."""
        prev = None
        cur  = self.head
        while cur is not None:
            if cur is target:
                if prev is None:
                    self.head = cur.tag_links[self.tag_name]
                else:
                    prev.tag_links[self.tag_name] = cur.tag_links[self.tag_name]
                cur.tag_links.pop(self.tag_name, None)
                self.size -= 1
                return
            prev = cur
            cur  = cur.tag_links[self.tag_name]

    def traverse(self) -> list[NoteNode]:
        """Kembalikan semua note dalam chain ini."""
        result = []
        cur = self.head
        while cur is not None:
            result.append(cur)
            cur = cur.tag_links[self.tag_name]
        return result


# ─── Note Collection (Multi-Linked) ──────────────────────────────────────────

class NoteCollection:
    """
    Koleksi note dengan dukungan multi-tag.
    tag_chains["python"] = TagChain yang memuat semua note bertag "python".
    """

    def __init__(self):
        self._notes:      dict[int, NoteNode]  = {}   # id → node
        self._tag_chains: dict[str, TagChain]  = {}   # tag → chain
        self._next_id = 1

    # ── Public API ────────────────────────────────────────────────────────────

    def add_note(self, title: str, content: str, tags: list[str]) -> NoteNode:
        """
        Buat note baru dan masukkan ke semua chain tag-nya.
        O(k) di mana k = jumlah tag.
        """
        node = NoteNode(self._next_id, title, content, tags)
        self._next_id += 1
        self._notes[node.note_id] = node

        for tag in tags:
            if tag not in self._tag_chains:
                self._tag_chains[tag] = TagChain(tag)
            self._tag_chains[tag].insert(node)

        return node

    def delete_note(self, note_id: int) -> None:
        """
        Hapus note dari SEMUA chain tag-nya sebelum dealokasi.
        Kunci Multi-Linked: wajib hapus dari semua chain dulu!
        """
        node = self._notes.pop(note_id, None)
        if node is None:
            print(f"Note id={note_id} tidak ditemukan.")
            return
        for tag in list(node.tags):
            if tag in self._tag_chains:
                self._tag_chains[tag].remove(node)

    def get_by_tag(self, tag: str) -> list[NoteNode]:
        """Ambil semua note dengan tag tertentu."""
        if tag not in self._tag_chains:
            return []
        return self._tag_chains[tag].traverse()

    def list_tags(self) -> list[str]:
        return list(self._tag_chains.keys())


# ─── Demo ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    col = NoteCollection()

    n1 = col.add_note("Belajar Python",   "print('hello')",        ["python", "belajar"])
    n2 = col.add_note("Linked List DLL",  "prev & next pointer",   ["python", "struktur-data"])
    n3 = col.add_note("Resep Nasi Goreng","bumbu rahasia...",       ["kuliner"])
    n4 = col.add_note("Binary Search",    "O(log n) search",       ["python", "struktur-data", "belajar"])

    print("=== Notes bertag 'python' ===")
    for n in col.get_by_tag("python"):
        print(" ", n)

    print("\n=== Notes bertag 'struktur-data' ===")
    for n in col.get_by_tag("struktur-data"):
        print(" ", n)

    print("\n=== Notes bertag 'belajar' ===")
    for n in col.get_by_tag("belajar"):
        print(" ", n)

    # Hapus n1 → harus hilang dari chain 'python' DAN 'belajar'
    print(f"\n--- Hapus note id={n1.note_id} ---")
    col.delete_note(n1.note_id)

    print("=== Notes bertag 'python' setelah delete ===")
    for n in col.get_by_tag("python"):
        print(" ", n)

    print("=== Notes bertag 'belajar' setelah delete ===")
    for n in col.get_by_tag("belajar"):
        print(" ", n)
