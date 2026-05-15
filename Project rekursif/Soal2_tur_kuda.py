"""
Tugas 2: Knight's Tour (Tur Kuda)
==================================
Menemukan urutan langkah kuda di papan catur NxN sehingga
setiap petak dikunjungi tepat satu kali.
Menggunakan algoritma backtracking rekursif + heuristik Warnsdorff.
"""


# 8 kemungkinan gerak kuda (dx, dy)
MOVES_X = [2, 1, -1, -2, -2, -1,  1,  2]
MOVES_Y = [1, 2,  2,  1, -1, -2, -2, -1]


def is_valid(x, y, board, n):
    """Memeriksa apakah posisi (x, y) valid dan belum dikunjungi."""
    return 0 <= x < n and 0 <= y < n and board[x][y] == -1


def get_degree(x, y, board, n):
    """
    Heuristik Warnsdorff: menghitung jumlah langkah valid dari (x, y).
    Memilih langkah dengan derajat terkecil → meningkatkan efisiensi.
    """
    count = 0
    for i in range(8):
        nx, ny = x + MOVES_X[i], y + MOVES_Y[i]
        if is_valid(nx, ny, board, n):
            count += 1
    return count


def solve_knights_tour(x, y, move_num, board, n):
    """
    Fungsi rekursif backtracking untuk Tur Kuda.
    x, y       : posisi kuda saat ini
    move_num   : urutan langkah ke-berapa (mulai dari 1)
    board      : papan berisi urutan kunjungan (-1 = belum dikunjungi)
    """
    # Base case: semua petak sudah dikunjungi
    if move_num == n * n + 1:
        return True

    # Kumpulkan semua langkah valid, urutkan berdasarkan heuristik Warnsdorff
    next_moves = []
    for i in range(8):
        nx, ny = x + MOVES_X[i], y + MOVES_Y[i]
        if is_valid(nx, ny, board, n):
            degree = get_degree(nx, ny, board, n)
            next_moves.append((degree, nx, ny))

    # Urutkan: pilih langkah dengan paling sedikit opsi selanjutnya
    next_moves.sort()

    for _, nx, ny in next_moves:
        board[nx][ny] = move_num          # tandai langkah ke-move_num
        if solve_knights_tour(nx, ny, move_num + 1, board, n):
            return True
        board[nx][ny] = -1                # backtrack

    return False


def print_board(board, n):
    """Mencetak papan dengan urutan langkah kuda."""
    cell_width = len(str(n * n)) + 2
    border = "+" + (("-" * cell_width + "+") * n)

    print(border)
    for row in range(n):
        row_str = "|"
        for col in range(n):
            num = str(board[row][col]).center(cell_width)
            row_str += num + "|"
        print(row_str)
        print(border)


def print_move_sequence(board, n):
    """Mencetak urutan langkah sebagai daftar koordinat."""
    total = n * n
    # Buat mapping: urutan langkah → (baris, kolom)
    sequence = [None] * (total + 1)
    for r in range(n):
        for c in range(n):
            sequence[board[r][c]] = (r, c)

    print("\nUrutan langkah kuda:")
    print("-" * 40)
    for step in range(total):
        r, c = sequence[step]
        arrow = " → " if step < total - 1 else ""
        # Cetak 5 langkah per baris
        end_char = "\n" if (step + 1) % 5 == 0 else ""
        print(f"({r},{c}){arrow}", end=end_char)
    print()


def main():
    print("=" * 45)
    print("     MASALAH TUR KUDA (KNIGHT'S TOUR)")
    print("=" * 45)

    while True:
        try:
            n = int(input("\nMasukkan ukuran papan (N, disarankan 5-8): "))
            if n < 5:
                print("Papan minimal ukuran 5x5.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan bilangan bulat positif.")

    while True:
        try:
            print(f"\nPosisi awal kuda (baris dan kolom dalam rentang 0 sampai {n-1}):")
            start_row = int(input("  Baris awal : "))
            start_col = int(input("  Kolom awal : "))
            if not (0 <= start_row < n and 0 <= start_col < n):
                print(f"Posisi harus dalam rentang 0 sampai {n-1}.")
                continue
            break
        except ValueError:
            print("Input tidak valid. Masukkan bilangan bulat.")

    # Inisialisasi papan: -1 = belum dikunjungi
    board = [[-1] * n for _ in range(n)]
    board[start_row][start_col] = 0   # langkah ke-0 = posisi awal

    print(f"\nMencari solusi Tur Kuda untuk papan {n}x{n}")
    print(f"Posisi awal: ({start_row}, {start_col})")
    print("Harap tunggu...")

    if solve_knights_tour(start_row, start_col, 1, board, n):
        print("\n✓ Solusi ditemukan!\n")
        print("Papan dengan urutan langkah kuda:\n")
        print_board(board, n)
        print_move_sequence(board, n)
    else:
        print(f"\n✗ Tidak ada solusi untuk papan {n}x{n}")
        print(f"  dengan posisi awal ({start_row}, {start_col}).")


if __name__ == "__main__":
    main()
