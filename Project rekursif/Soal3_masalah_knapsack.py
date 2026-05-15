"""
Tugas 3: Knapsack Problem (Masalah Knapsack)
=============================================
Mencari kombinasi barang yang bisa dimasukkan ke dalam knapsack
untuk mencapai berat target (tidak melebihi batas maksimum).
Menggunakan algoritma rekursif dengan backtracking.
"""


def knapsack_recursive(items, target, index, current_weight, current_items, solutions):
    """
    Algoritma rekursif untuk menyelesaikan Knapsack Problem.

    Parameter:
        items          : list berat barang yang tersedia
        target         : berat maksimum knapsack
        index          : indeks barang yang sedang dipertimbangkan
        current_weight : total berat barang yang sudah dipilih
        current_items  : list indeks barang yang sudah dipilih
        solutions      : list untuk menyimpan semua solusi yang ditemukan
    """
    # Base case: semua barang sudah dipertimbangkan
    if index == len(items):
        if current_weight <= target and current_weight > 0:
            solutions.append((current_weight, current_items[:]))
        return

    # === Cabang 1: MASUKKAN barang ke-index ke dalam knapsack ===
    new_weight = current_weight + items[index]
    if new_weight <= target:                      # hanya jika tidak melebihi target
        current_items.append(index)
        knapsack_recursive(items, target, index + 1,
                           new_weight, current_items, solutions)
        current_items.pop()                       # backtrack

    # === Cabang 2: LEWATI barang ke-index (tidak dimasukkan) ===
    knapsack_recursive(items, target, index + 1,
                       current_weight, current_items, solutions)


def knapsack_exact(items, target, index, current_weight, current_items):
    """
    Versi rekursif yang mencari solusi TEPAT sama dengan target.
    Mengembalikan solusi pertama yang ditemukan (atau None).
    """
    # Base case: berat tepat sama dengan target → solusi ditemukan!
    if current_weight == target:
        return current_items[:]

    # Tidak ada barang tersisa atau kelebihan berat
    if index == len(items) or current_weight > target:
        return None

    # Cabang 1: masukkan barang ke-index
    current_items.append(index)
    result = knapsack_exact(items, target, index + 1,
                            current_weight + items[index], current_items)
    if result is not None:
        return result
    current_items.pop()   # backtrack

    # Cabang 2: lewati barang ke-index
    return knapsack_exact(items, target, index + 1,
                          current_weight, current_items)


def display_solution(items, solution_indices, target):
    """Menampilkan detail solusi yang ditemukan."""
    chosen = [items[i] for i in solution_indices]
    total = sum(chosen)

    print(f"  Barang dipilih (indeks) : {[i+1 for i in solution_indices]}")
    print(f"  Berat masing-masing     : {chosen}")
    print(f"  Total berat             : {total} / {target}")
    print(f"  Sisa kapasitas          : {target - total}")


def input_items_manual(n):
    """Meminta pengguna memasukkan berat barang satu per satu."""
    items = []
    print(f"\nMasukkan berat {n} barang:")
    for i in range(n):
        while True:
            try:
                w = float(input(f"  Berat barang ke-{i+1}: "))
                if w <= 0:
                    print("  Berat harus lebih dari 0.")
                    continue
                items.append(w)
                break
            except ValueError:
                print("  Input tidak valid.")
    return items


def main():
    print("=" * 50)
    print("     MASALAH KNAPSACK (REKURSIF)")
    print("=" * 50)
    print("\nContoh soal dari tugas:")
    print("  Barang  : [2, 5, 6, 9, 12, 14, 20]")
    print("  Target  : 30")
    print("  Salah satu solusi: [2, 5, 9, 14] = 30\n")

    print("Pilih mode input:")
    print("  1. Gunakan contoh soal (default)")
    print("  2. Masukkan data sendiri")

    choice = input("\nPilihan (1/2): ").strip()

    if choice == "2":
        while True:
            try:
                n = int(input("Jumlah barang: "))
                if n < 1:
                    print("Jumlah barang minimal 1.")
                    continue
                break
            except ValueError:
                print("Input tidak valid.")

        items = input_items_manual(n)

        while True:
            try:
                target = float(input("Masukkan berat target knapsack: "))
                if target <= 0:
                    print("Target harus lebih dari 0.")
                    continue
                break
            except ValueError:
                print("Input tidak valid.")
    else:
        # Gunakan contoh dari soal
        items = [2, 5, 6, 9, 12, 14, 20]
        target = 30
        print(f"\n[Menggunakan contoh soal]")
        print(f"Barang : {items}")
        print(f"Target : {target}")

    print(f"\n{'='*50}")
    print(f"Mencari kombinasi dengan total berat = {target}...")
    print(f"{'='*50}")

    # --- Cari satu solusi tepat ---
    exact_solution = knapsack_exact(items, target, 0, 0, [])

    if exact_solution:
        print("\n✓ Solusi tepat ditemukan (berat = target):")
        display_solution(items, exact_solution, target)
    else:
        print(f"\n✗ Tidak ada kombinasi dengan total berat TEPAT {target}.")

    # --- Cari semua solusi (berat ≤ target) ---
    print(f"\n{'='*50}")
    print(f"Mencari semua kombinasi dengan berat ≤ {target}...")
    print(f"{'='*50}")

    all_solutions = []
    knapsack_recursive(items, target, 0, 0, [], all_solutions)

    if all_solutions:
        # Urutkan berdasarkan berat (terbesar dulu)
        all_solutions.sort(key=lambda x: x[0], reverse=True)

        print(f"\nDitemukan {len(all_solutions)} kombinasi valid.")

        # Tampilkan top 5 solusi dengan berat terbesar
        top_n = min(5, len(all_solutions))
        print(f"\nTop {top_n} kombinasi terbaik (berat terbesar):")
        print("-" * 50)

        for rank, (weight, indices) in enumerate(all_solutions[:top_n], 1):
            chosen = [items[i] for i in indices]
            print(f"\n  Ranking ke-{rank} (berat = {weight}):")
            display_solution(items, indices, target)

        # Statistik
        print(f"\n{'='*50}")
        print(f"STATISTIK:")
        print(f"  Total kombinasi valid : {len(all_solutions)}")
        print(f"  Berat terbesar        : {all_solutions[0][0]}")
        print(f"  Berat terkecil        : {all_solutions[-1][0]}")
        avg = sum(w for w, _ in all_solutions) / len(all_solutions)
        print(f"  Rata-rata berat       : {avg:.2f}")
    else:
        print(f"\n✗ Tidak ada kombinasi barang yang memenuhi syarat.")


if __name__ == "__main__":
    main()
