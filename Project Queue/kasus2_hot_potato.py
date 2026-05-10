"""
kasus2_hot_potato.py — Permainan Hot Potato
============================================
Aturan permainan:
  - Pemain duduk melingkar dan mengoper benda.
  - Setelah N kali oper, pemain yang memegang benda tersingkir.
  - Ulangi sampai tersisa 1 orang → pemenang!

Teknik kunci:
  dequeue() lalu enqueue() kembali = simulasi oper melingkar.
  Setelah num kali oper, dequeue() tanpa enqueue() = tersingkir.
"""

from queue import Queue


def hot_potato(names: list[str], num: int, verbose: bool = True) -> str:
    """
    Simulasi permainan Hot Potato.

    Parameters
    ----------
    names   : daftar nama pemain
    num     : jumlah oper sebelum seseorang tersingkir
    verbose : cetak log tiap putaran

    Returns
    -------
    Nama pemenang (str)
    """
    q = Queue(max_size=len(names) + 1)
    for name in names:
        q.enqueue(name)

    ronde = 0
    if verbose:
        print(f"  Pemain awal : {names}")
        print(f"  Oper per ronde : {num}\n")

    while len(q) > 1:
        ronde += 1
        # Oper: putar queue sebanyak `num` kali
        for _ in range(num):
            q.enqueue(q.dequeue())

        # Pemain paling depan tersingkir
        tersingkir = q.dequeue()

        sisa = []
        for i in range(len(q)):
            item = q.dequeue()
            sisa.append(item)
            q.enqueue(item)

        if verbose:
            print(f"  Ronde {ronde:2d} | Tersingkir: {tersingkir:<10} "
                  f"| Sisa: {sisa}")

    pemenang = q.dequeue()
    if verbose:
        print(f"\n  🏆  Pemenang: {pemenang}")
    return pemenang


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KASUS 2: Permainan Hot Potato")
    print("=" * 55)

    pemain = ["Andi", "Budi", "Citra", "Dedi", "Eka", "Fani", "Gita", "Hadi"]

    print("\n--- Oper 3 kali per ronde ---")
    hot_potato(pemain, num=3)

    print("\n--- Oper 7 kali per ronde (hasil berbeda) ---")
    hot_potato(pemain, num=7)

    # Uji dengan kelompok kecil
    print("\n--- 4 pemain, oper 5 kali ---")
    hot_potato(["Alice", "Bob", "Charlie", "Diana"], num=5)
