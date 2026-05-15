"""
Tugas 1: N-Queens Problem (Masalah N-Ratu)
==========================================
Menyelesaikan masalah penempatan N ratu di papan NxN sehingga
tidak ada dua ratu yang saling menyerang (baris, kolom, diagonal).
Menggunakan algoritma backtracking rekursif.
"""


def is_safe(board, row, col, n):
    """
    Memeriksa apakah aman menempatkan ratu di posisi (row, col).
    Memeriksa kolom dan diagonal (tidak perlu cek baris karena
    kita menempatkan satu ratu per baris).
    """
    # Cek kolom yang sama di baris-baris sebelumnya
    for i in range(row):
        if board[i] == col:
            return False

    # Cek diagonal kiri atas
    i, j = row - 1, col - 1
    while i >= 0 and j >= 0:
        if board[i] == j:
            return False
        i -= 1
        j -= 1

    # Cek diagonal kanan atas
    i, j = row - 1, col + 1
    while i >= 0 and j < n:
        if board[i] == j:
            return False
        i -= 1
        j += 1

    return True


def solve_nqueens(board, row, n, solutions):
    """
    Fungsi rekursif untuk menyelesaikan N-Queens.
    board[i] = kolom tempat ratu di baris i diletakkan.
    """
    # Base case: semua baris sudah diisi → solusi ditemukan
    if row == n:
        solutions.append(board[:])  # simpan salinan solusi
        return

    for col in range(n):
        if is_safe(board, row, col, n):
            board[row] = col              # tempatkan ratu
            solve_nqueens(board, row + 1, n, solutions)  # rekursi ke baris berikutnya
            board[row] = -1               # backtrack: hapus ratu


def print_board(solution, n):
    """Mencetak papan catur dengan posisi ratu."""
    border = "+" + ("---+" * n)
    print(border)
    for row in range(n):
        row_str = "|"
        for col in range(n):
            if solution[row] == col:
                row_str += " Q |"
            else:
                row_str += " . |"
        print(row_str)
        print(border)


def main():
    print("=" * 45)
    print("       MASALAH N-QUEENS (N-RATU)")
    print("=" * 45)

    while True:
        try:
            n = int(input("\nMasukkan ukuran papan (N): "))
            if n < 1:
                print("Ukuran papan harus minimal 1.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan bilangan bulat positif.")

    board = [-1] * n
    solutions = []

    print(f"\nMencari solusi untuk {n}-Queens...")
    solve_nqueens(board, 0, n, solutions)

    if not solutions:
        print(f"\nTidak ada solusi untuk {n}-Queens.")
    else:
        print(f"\nDitemukan {len(solutions)} solusi!")
        print("\nMenampilkan solusi pertama:\n")
        print_board(solutions[0], n)

        # Tampilkan semua solusi jika n kecil
        if n <= 6 and len(solutions) > 1:
            tampil = input(f"\nTampilkan semua {len(solutions)} solusi? (y/n): ").strip().lower()
            if tampil == 'y':
                for idx, sol in enumerate(solutions, 1):
                    print(f"\nSolusi ke-{idx}:")
                    print_board(sol, n)

        print(f"\nRingkasan: {n}-Queens memiliki {len(solutions)} solusi.")


if __name__ == "__main__":
    main()
