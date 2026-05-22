"""
expr_heap_sorter.py
===================
Implementasi ExprHeapSorter untuk Tugas Teori & Analisis Algoritma Binary Tree.

Modul ini mengimplementasikan:
  1. Expression Tree Builder & Evaluator
     - Menerima ekspresi aritmetika terparentheses penuh (fully parenthesized)
     - Dibangun menggunakan antrian token (deque) + rekursi
     - Evaluasi postorder
     - Handle pembagian nol & token tidak valid
  2. In-Place Max-Heap Construction
     - Mengubah list integer menjadi max-heap tanpa alokasi array tambahan
  3. Heapsort In-Place
     - Mengurutkan ascending menggunakan ekstraksi root + sift-down
  4. Complete Tree Validator
     - Memverifikasi apakah array memenuhi properti complete binary tree

Batasan yang dipenuhi:
  - Dilarang list.sort(), sorted(), heapq, library eksternal
  - Heap & Sort benar-benar in-place (hanya variabel indeks & counter)
  - Tidak ada array/list tambahan selama sorting
"""

from typing import List, Optional
from collections import deque


# =============================================================================
# EXPRESSION HEAP SORTER
# =============================================================================

class ExprHeapSorter:
    """
    Menggabungkan tiga modul dari Bab 13:
      - Expression Tree Builder & Evaluator
      - In-Place Max-Heap Construction
      - Heapsort In-Place
      - Complete Tree Validator
    """

    OPERATORS = set(['+', '-', '*', '/'])

    def __init__(self, expr_str: str):
        """
        Parameters:
            expr_str: ekspresi aritmetika terparentheses penuh,
                      contoh: "((8 * 5) + (9 / (7 - 4)))"
        """
        self.expr = expr_str
        self.values: List[int] = []

    # =========================================================================
    # 1. EXPRESSION TREE
    # =========================================================================

    def parse_and_evaluate(self) -> List[int]:
        """
        Tokenisasi → Bangun pohon ekspresi → Evaluasi → Kembalikan list nilai.

        Mengapa mengembalikan List?
        Karena ekspresi dapat mengandung sub-ekspresi yang nilainya dikumpulkan
        untuk dimasukkan ke heap. Dalam implementasi ini, kita mengembalikan
        [nilai_root] (nilai akhir ekspresi).

        Returns:
            List berisi satu nilai integer (hasil evaluasi ekspresi).
        """
        tokens = self._tokenize(self.expr)
        root = self._build_tree(tokens)
        value = self._eval_tree(root)
        self.values = [int(value)]
        return self.values

    def _tokenize(self, expr: str) -> deque:
        """
        Tokenisasi ekspresi menjadi deque token.

        Token yang dikenali:
          - '(' dan ')': tanda kurung
          - '+', '-', '*', '/': operator
          - Angka multi-digit (misalnya '10', '42')
          - Spasi diabaikan

        Returns:
            deque berisi token-token string.
        """
        tokens = deque()
        i = 0
        while i < len(expr):
            ch = expr[i]
            if ch == ' ':
                i += 1
                continue
            if ch in ('(', ')') or ch in self.OPERATORS:
                tokens.append(ch)
                i += 1
            elif ch.isdigit():
                # Baca angka multi-digit
                j = i
                while j < len(expr) and expr[j].isdigit():
                    j += 1
                tokens.append(expr[i:j])
                i = j
            else:
                raise ValueError(f"Token tidak valid: '{ch}' pada posisi {i}")
        return tokens

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Bangun pohon ekspresi secara rekursif dari antrian token.

        Format node (dict):
            {'val': operator_atau_operand, 'left': node_kiri, 'right': node_kanan}

        Algoritma (sesuai Listing 13.9):
          - Jika token berikutnya '(' → ini adalah sub-ekspresi:
              1. Konsumsi '('
              2. Rekursi untuk membuat subtree kiri
              3. Token berikutnya adalah operator → simpan di node root
              4. Rekursi untuk membuat subtree kanan
              5. Konsumsi ')' (diabaikan)
          - Jika bukan '(' → ini adalah operand (angka), buat leaf node.

        Mengapa rekursi cocok?
        Struktur ekspresi terparentheses penuh adalah rekursif secara alami:
        setiap ( membuka sub-ekspresi yang bisa berisi sub-ekspresi lagi.

        Returns:
            Root node dari pohon ekspresi (dict).
        """
        if not tokens:
            raise ValueError("Token habis sebelum ekspresi selesai")

        token = tokens.popleft()

        if token == '(':
            # Sub-ekspresi: ( left op right )
            left = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Operator tidak ditemukan setelah operand kiri")
            operator = tokens.popleft()
            if operator not in self.OPERATORS:
                raise ValueError(f"Token '{operator}' bukan operator yang valid")

            right = self._build_tree(tokens)

            if not tokens:
                raise ValueError("Tanda ')' penutup tidak ditemukan")
            closing = tokens.popleft()
            if closing != ')':
                raise ValueError(f"Diharapkan ')', ditemukan '{closing}'")

            return {'val': operator, 'left': left, 'right': right}

        elif token == ')':
            raise ValueError("Tanda ')' tidak terduga")

        elif token in self.OPERATORS:
            raise ValueError(f"Operator '{token}' tidak terduga di posisi ini")

        else:
            # Operand (angka) → leaf node
            try:
                return {'val': int(token), 'left': None, 'right': None}
            except ValueError:
                raise ValueError(f"Token '{token}' bukan angka atau operator valid")

    def _eval_tree(self, node: Optional[dict]) -> float:
        """
        Evaluasi pohon ekspresi secara POSTORDER (left → right → root).

        Traversal Postorder menghasilkan urutan evaluasi yang benar karena:
        - Kita harus tahu nilai operand kiri dan kanan sebelum menerapkan operator.
        - Postorder: kunjungi kiri, kunjungi kanan, proses root.
        - Ini secara otomatis menghasilkan notasi postfix.

        Contoh ((8 * 5) + (9 / (7 - 4))):
          Pohon:     +
                   /   \
                 *       /
                / \     / \
               8   5   9   -
                          / \
                         7   4

          Postorder: 8 5 * 9 7 4 - / +  ← notasi postfix valid

        Mengapa postorder otomatis benar?
        Karena dalam pohon ekspresi, operator SELALU di atas operandnya.
        Postorder memastikan operand sudah dievaluasi sebelum operatornya diproses.

        Parameters:
            node: node pohon ekspresi (dict) atau None

        Returns:
            Nilai numerik hasil evaluasi.

        Raises:
            ValueError: jika terjadi pembagian nol.
        """
        if node is None:
            raise ValueError("Node kosong tidak dapat dievaluasi")

        # Leaf node (operand)
        if node['left'] is None and node['right'] is None:
            return float(node['val'])

        # Internal node (operator)
        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])
        op = node['val']

        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Pembagian nol terdeteksi!")
            return left_val / right_val
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    def _postorder_string(self, node: Optional[dict]) -> str:
        """
        Menghasilkan notasi postfix dari pohon ekspresi.
        Digunakan untuk demonstrasi/verifikasi.
        """
        if node is None:
            return ""
        left = self._postorder_string(node['left'])
        right = self._postorder_string(node['right'])
        val = str(node['val'])
        parts = [p for p in [left, right, val] if p]
        return " ".join(parts)

    def _inorder_string(self, node: Optional[dict]) -> str:
        """
        Menghasilkan notasi infix dari pohon ekspresi.
        Inorder MEMERLUKAN tanda kurung eksplisit agar urutan operasi benar,
        berbeda dengan postorder yang tidak memerlukannya.
        """
        if node is None:
            return ""
        if node['left'] is None and node['right'] is None:
            return str(node['val'])
        left = self._inorder_string(node['left'])
        right = self._inorder_string(node['right'])
        return f"({left} {node['val']} {right})"

    # =========================================================================
    # 2 & 3. HEAPSORT IN-PLACE
    # =========================================================================

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array secara ascending menggunakan In-Place Heapsort.

        Algoritma (dua fase):
        Fase 1 – Build Max-Heap:
          - Mulai dari node non-leaf terakhir (indeks n//2 - 1) ke indeks 0.
          - Panggil sift-down pada setiap node untuk memastikan heap order property.
          - Mengapa dari n//2 - 1? Karena node dengan indeks >= n//2 adalah leaf
            (tidak punya anak), sehingga sudah trivially valid sebagai heap.
          - Kompleksitas: O(n) — bukan O(n log n)! (Hasil analisis amortized)

        Fase 2 – Ekstraksi Berulang:
          - Swap root (elemen terbesar) ke posisi akhir array.
          - Kurangi ukuran heap (heap_size -= 1, secara virtual).
          - Sift-down root baru untuk memulihkan heap order.
          - Ulangi sampai heap hanya berisi 1 elemen.
          - Kompleksitas: O(n log n)

        Mengapa tetap O(n log n) meski swap berulang pada array yang sama?
        Fase 2 melakukan n-1 ekstraksi, dan setiap sift-down membutuhkan paling
        banyak O(log n) perbandingan (tinggi heap). Total: O(n log n).

        In-place: tidak ada array tambahan, hanya variabel indeks.

        Returns:
            arr yang sudah terurut ascending (in-place, array yang sama).
        """
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Build max-heap dari bawah ke atas
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Ekstraksi elemen terbesar satu per satu
        for end in range(n - 1, 0, -1):
            # Swap root (max) ke posisi end
            arr[0], arr[end] = arr[end], arr[0]
            # Sift-down pada heap yang diperkecil (ukuran = end)
            self._sift_down(arr, end, 0)

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Pulihkan heap order property mulai dari idx ke bawah.

        Cara kerja:
        - Hitung indeks anak kiri (left = 2*idx + 1) dan kanan (right = 2*idx + 2).
        - Cari indeks elemen terbesar di antara arr[idx], arr[left], arr[right].
        - Jika largest != idx → swap, lalu lanjutkan sift-down ke bawah.
        - Berhenti jika largest == idx (sudah di posisi yang benar).

        Rumus indeks valid untuk Complete Binary Tree:
        - Rumus left = 2*i + 1 dan right = 2*i + 2 HANYA valid jika pohon adalah
          complete binary tree (semua level penuh kecuali mungkin level terakhir,
          diisi dari kiri). Complete binary tree menjamin tidak ada "lubang" dalam
          pemetaan array ke indeks, sehingga rumus aritmetika ini konsisten.

        Jumlah perbandingan maksimum satu sift-down untuk heap ukuran n:
        - Tinggi heap h = floor(log2(n))
        - Setiap level: 2 perbandingan (arr[idx] vs arr[left], lalu vs arr[right])
        - Maksimum: 2 * floor(log2(n)) perbandingan

        Parameters:
            arr: array heap
            heap_size: ukuran heap aktif (elemen setelah indeks ini diabaikan)
            idx: indeks node yang akan di-sift-down
        """
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            # Bandingkan dengan anak kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Bandingkan dengan anak kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika idx sudah yang terbesar, heap order terpenuhi
            if largest == idx:
                break

            # Swap dan lanjutkan ke bawah
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    # =========================================================================
    # 4. COMPLETE TREE VALIDATOR
    # =========================================================================

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Validasi apakah array memenuhi properti Complete Binary Tree
        ketika dipetakan ke struktur heap.

        Definisi Complete Binary Tree:
        - Semua level penuh kecuali mungkin level terakhir.
        - Level terakhir diisi dari KIRI ke KANAN (tidak ada "lubang").

        Cara memvalidasi dengan pemetaan array:
        - Jika array memiliki n elemen, node valid adalah indeks 0 sampai n-1.
        - Untuk setiap node di indeks i:
            * Anak kiri ada di indeks 2*i + 1
            * Anak kanan ada di indeks 2*i + 2
        - Jika ada node dengan anak kiri yang tidak ada (2*i+1 >= n) tetapi
          anak kanannya ada (2*i+2 < n) → ada "lubang" → BUKAN complete tree.
        - Begitu kita menemukan node pertama yang tidak punya anak kiri,
          semua node berikutnya harus berupa leaf (tidak punya anak sama sekali).

        Catatan: Array yang dihasilkan oleh heapsort inplace BUKAN complete tree
        dalam arti heap, karena elemen sudah dipindah ke posisi akhir.
        Array yang valid sebagai complete binary tree adalah array sebelum sort
        (setelah fase Build Max-Heap) atau array yang dibangun dari BFS traversal.

        Returns:
            True jika complete binary tree, False jika tidak.
        """
        n = len(arr)
        if n == 0:
            return True

        # Flag: sudah ditemukan node tanpa anak kiri?
        found_incomplete = False

        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            has_left = left < n
            has_right = right < n

            if found_incomplete:
                # Setelah node tidak punya anak kiri, tidak boleh ada node dengan anak
                if has_left or has_right:
                    return False
            else:
                if not has_left:
                    # Node ini tidak punya anak kiri
                    # Anak kanan juga tidak boleh ada
                    if has_right:
                        return False
                    found_incomplete = True
                else:
                    if not has_right:
                        # Punya kiri tapi tidak kanan → anak berikutnya harus leaf
                        found_incomplete = True

        return True


# =============================================================================
# DEMO & TEST
# =============================================================================

if __name__ == "__main__":

    print("=" * 65)
    print("1. EXPRESSION TREE BUILDER & EVALUATOR")
    print("=" * 65)

    test_exprs = [
        "((8 * 5) + (9 / (7 - 4)))",     # Dari soal: 40 + 3 = 43
        "((3 + 4) * (2 - 1))",             # 7 * 1 = 7
        "((10 / 2) + (3 * 4))",            # 5 + 12 = 17
        "(5 + 3)",                          # Sederhana: 8
    ]

    for expr in test_exprs:
        try:
            sorter = ExprHeapSorter(expr)
            tokens = sorter._tokenize(expr)
            tokens_copy = tokens.copy()
            root = sorter._build_tree(tokens_copy)
            result = sorter._eval_tree(root)

            tokens2 = sorter._tokenize(expr)
            root2 = sorter._build_tree(tokens2)

            print(f"  Ekspresi  : {expr}")
            print(f"  Postfix   : {sorter._postorder_string(root2)}")
            tokens3 = sorter._tokenize(expr)
            root3 = sorter._build_tree(tokens3)
            print(f"  Infix     : {sorter._inorder_string(root3)}")
            print(f"  Hasil     : {result}")
            print()
        except ValueError as e:
            print(f"  ERROR: {e}")
            print()

    # Test pembagian nol
    print("  Test pembagian nol: (8 / (4 - 4))")
    try:
        s = ExprHeapSorter("(8 / (4 - 4))")
        toks = s._tokenize("(8 / (4 - 4))")
        r = s._build_tree(toks)
        s._eval_tree(r)
    except ValueError as e:
        print(f"  Berhasil ditangkap: {e}")
    print()

    print("=" * 65)
    print("2 & 3. HEAPSORT IN-PLACE")
    print("=" * 65)

    sorter_main = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")

    heap_tests = [
        [38, 27, 43, 3, 9, 82, 10],
        [5, 5, 3, 3, 1, 1],
        [1],
        [],
        list(range(10, 0, -1)),
        [100, 1, 50, 25, 75],
    ]

    for tc in heap_tests:
        original = tc[:]
        result = sorter_main.heapsort_inplace(tc)
        print(f"  Input : {original}")
        print(f"  Output: {result}")
        print()

    print("=" * 65)
    print("4. COMPLETE TREE VALIDATOR")
    print("=" * 65)

    # Complete binary tree: [1, 2, 3, 4, 5] → level 0: [1], level 1: [2,3], level 2: [4,5]
    arrays = [
        ([1, 2, 3, 4, 5], "Complete tree (valid)"),
        ([1, 2, 3, 4, 5, 6, 7], "Complete tree penuh (valid)"),
        ([1, 2, 3, 4, 5, 6], "Level terakhir tidak lengkap tapi dari kiri (valid)"),
        ([1], "Single node (valid)"),
        ([], "Kosong (valid)"),
        ([10, 8, 6, 4, 2], "Array setelah sort DESC ← ini bukan complete tree yang valid sebagai heap"),
    ]

    for arr, desc in arrays:
        s = ExprHeapSorter("")
        result = s.is_complete_tree(arr)
        print(f"  {desc}")
        print(f"  Array : {arr}")
        print(f"  Result: {'✓ Complete Tree' if result else '✗ Bukan Complete Tree'}")
        print()

    print("=" * 65)
    print("INTEGRASI: Parse → Heap → Sort")
    print("=" * 65)

    # Evaluasi ekspresi dari soal, lalu sort list bilangan
    expr = "((8 * 5) + (9 / (7 - 4)))"
    data = [15, 3, 42, 8, 27, 1, 99, 11]

    sorter_int = ExprHeapSorter(expr)
    expr_val = sorter_int.parse_and_evaluate()
    combined = data + expr_val
    print(f"  Nilai ekspresi '{expr}' = {expr_val[0]}")
    print(f"  Data awal + nilai ekspresi: {combined}")

    sorter_int.heapsort_inplace(combined)
    print(f"  Setelah heapsort: {combined}")
