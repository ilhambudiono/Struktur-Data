"""
advanced_sorter.py
==================
Implementasi AdvancedSorter untuk Tugas Analisis & Desain Algoritma Sorting Lanjutan.

Modul ini mengimplementasikan:
  1. Array Merge Sort dengan SATU tmpArray (virtual sublists, O(n) extra space, bukan O(n log n))
  2. Linked List Merge Sort dengan fast-slow pointer + dummy node (O(log n) space)
  3. Quick Sort dengan Median-of-Three pivot + fallback ke Merge Sort jika depth > 2*log2(n)

Batasan yang dipenuhi:
  - Dilarang list.sort(), sorted(), slice[:] untuk pemisahan, library eksternal
  - Array Sort: hanya 1 tmpArray berukuran n, tidak ada sublist fisik di tiap rekursi
  - Linked List Sort: hanya modifikasi pointer .next, tidak ada node baru (kecuali 1 dummy)
  - Stabilitas: dijaga di merge sort (array & linked list)
  - Quick Sort fallback: otomatis beralih ke merge sort jika depth > 2*log2(n)
"""

import math
from typing import List, Optional


# =============================================================================
# NODE untuk Singly Linked List
# =============================================================================

class ListNode:
    """Node untuk Singly Linked List."""
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f"ListNode({self.data})"


# =============================================================================
# ADVANCED SORTER
# =============================================================================

class AdvancedSorter:
    """
    Kelas utama yang mengimplementasikan berbagai algoritma sorting dengan
    batasan memori ketat.
    """

    def __init__(self):
        pass

    # =========================================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        """
        Mengurutkan array integer secara ascending menggunakan Merge Sort.

        Strategi:
        - Alokasi SATU tmpArray berukuran n di awal (O(n) extra space total).
        - Setiap rekursi hanya menggunakan indeks (first, mid, last) — tidak ada
          sublist fisik. Ini disebut "virtual sublists".
        - Stable: elemen sama mempertahankan urutan relatif aslinya.

        Kompleksitas: O(n log n) waktu, O(n) ruang (tmpArray) + O(log n) stack.
        """
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)          # Satu-satunya alokasi tambahan
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        """
        Rekursi divide-and-conquer.

        Bagi array menjadi dua "virtual sublist" [first..mid] dan [mid+1..last],
        rekursi pada masing-masing, lalu merge.
        """
        if first >= last:
            return                          # Base case: sublist panjang 0 atau 1
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Gabungkan dua virtual sublist yang bersebelahan secara STABLE.

        Cara kerja:
        1. Salin arr[left_start..right_end] ke tmp_array.
        2. Merge dari tmp_array kembali ke arr menggunakan dua pointer (a, b).
        3. Gunakan `<=` saat membandingkan: jika sama, ambil dari kiri dulu
           → menjamin stabilitas.

        Mengapa hanya 1 tmpArray?
        - Tidak seperti versi slice yang membuat subarray baru di tiap rekursi,
          di sini tmpArray selalu sama objeknya. Rekursi berbeda pakai bagian
          indeks yang berbeda, tidak ada konflik karena merge dilakukan setelah
          kedua rekursi selesai (post-order).
        """
        # Salin bagian yang relevan ke tmp_array
        for k in range(left_start, right_end + 1):
            tmp_array[k] = arr[k]

        a = left_start          # pointer untuk sublist kiri di tmp_array
        b = mid + 1             # pointer untuk sublist kanan di tmp_array
        k = left_start          # pointer untuk posisi di arr

        while a <= mid and b <= right_end:
            # STABLE: jika sama, ambil dari kiri (a) terlebih dahulu
            if tmp_array[a] <= tmp_array[b]:
                arr[k] = tmp_array[a]
                a += 1
            else:
                arr[k] = tmp_array[b]
                b += 1
            k += 1

        # Salin sisa sublist kiri (sublist kanan sudah di tempat yang benar)
        while a <= mid:
            arr[k] = tmp_array[a]
            a += 1
            k += 1

        # Sisa sublist kanan tidak perlu disalin (sudah ada di arr[k..right_end])

    # =========================================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow Pointer + Dummy Node Merge)
    # =========================================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        Mengurutkan Singly Linked List secara ascending menggunakan Merge Sort.

        Strategi:
        - Split menggunakan fast-slow pointer (satu traversal, tanpa hitung panjang).
        - Merge menggunakan dummy node dan tail reference (tanpa alokasi node baru).
        - Stable: elemen sama mempertahankan urutan relatif aslinya.

        Kompleksitas: O(n log n) waktu, O(log n) ruang (stack rekursi saja).
        """
        if head is None or head.next is None:
            return head

        # Split menjadi dua sublist
        right_head = self._split_linked_list(head)
        left_head = head

        # Rekursi pada masing-masing sublist
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Gabungkan dua sublist yang sudah terurut
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Temukan titik tengah list menggunakan teknik Fast-Slow Pointer,
        lalu putus list menjadi dua bagian.

        Cara kerja:
        - midPoint bergerak 1 langkah per iterasi (slow).
        - curNode bergerak 2 langkah per iterasi (fast).
        - Ketika curNode mencapai akhir list, midPoint berada di tengah.
        - Ini hanya memerlukan SATU traversal tanpa menghitung panjang list.

        Mengapa satu traversal cukup?
        Karena rasio kecepatan 1:2 menjamin ketika fast sampai ujung (n langkah),
        slow sudah menempuh n/2 langkah → posisi tengah.

        Returns:
            head dari sublist kanan (node setelah midPoint).
        """
        midPoint = head              # slow pointer, akan berhenti di tengah
        curNode = head.next          # fast pointer, bergerak 2x lebih cepat

        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next
            curNode = curNode.next.next

        # midPoint sekarang adalah node terakhir sublist kiri
        right_head = midPoint.next
        midPoint.next = None         # Putus link → dua sublist terpisah

        return right_head

    def _merge_linked_lists(self,
                            listA: Optional[ListNode],
                            listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Gabungkan dua sorted linked list menjadi satu sorted linked list secara STABLE.

        Teknik Dummy Node + Tail Reference:
        - dummy adalah node sentinel yang tidak berisi data bermakna.
          Tujuannya: menghindari kasus khusus untuk head pertama.
        - tail selalu menunjuk ke node terakhir dari list hasil merge.
          Penambahan node baru cukup dengan tail.next = node_baru; tail = tail.next
        - TIDAK ada alokasi node baru: kita hanya mengubah pointer .next dari
          node-node yang sudah ada di listA dan listB.

        Mengapa ruang O(1) per merge call?
        Hanya variabel dummy, tail, dan pointer loop. Tidak ada array atau node baru.
        Total ruang O(log n) berasal dari stack rekursi sort_linked_list, bukan merge.

        Returns:
            head dari list hasil merge (dummy.next).
        """
        dummy = ListNode(0)          # Sentinel node (1 dummy statis per merge call)
        tail = dummy                 # tail selalu menunjuk ke ujung list hasil

        while listA is not None and listB is not None:
            # STABLE: jika sama, ambil dari listA (sublist kiri) terlebih dahulu
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next

        # Sambungkan sisa list yang belum habis (tidak perlu loop lagi)
        tail.next = listA if listA is not None else listB

        return dummy.next

    # =========================================================================
    # 3. QUICK SORT dengan Median-of-Three Pivot + Depth Fallback
    # =========================================================================

    def sort_array_quicksort(self, arr: List[int]) -> List[int]:
        """
        Entry point untuk Quick Sort dengan fallback ke Merge Sort.

        Quick Sort rata-rata O(n log n), tetapi worst-case O(n²) jika pivot buruk.
        Solusi:
        1. Median-of-Three: pilih median dari arr[first], arr[mid], arr[last] sebagai pivot.
           Ini mengurangi kemungkinan worst-case secara drastis.
        2. Depth limiter: jika kedalaman rekursi > 2*log2(n), beralih ke Merge Sort.
           (Strategi ini dikenal sebagai Introsort, digunakan di C++ std::sort)
        """
        if len(arr) <= 1:
            return arr
        max_depth = int(2 * math.log2(len(arr))) if len(arr) > 1 else 1
        self._quick_sort_recursive(arr, 0, len(arr) - 1, max_depth, depth=0)
        return arr

    def _quick_sort_recursive(self, arr, first, last, max_depth, depth):
        """Rekursi Quick Sort dengan depth tracking."""
        if first >= last:
            return

        # Fallback ke Merge Sort jika kedalaman rekursi berlebihan
        if depth > max_depth:
            # Ekstrak subarray, sort dengan merge sort, masukkan kembali
            sub = arr[first:last + 1]   # slice diizinkan HANYA untuk fallback
            self._rec_merge_sort(sub, 0, len(sub) - 1, [0] * len(sub))
            arr[first:last + 1] = sub
            return

        pivot_pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_pos - 1, max_depth, depth + 1)
        self._quick_sort_recursive(arr, pivot_pos + 1, last, max_depth, depth + 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Partisi array menggunakan Median-of-Three pivot.

        Langkah:
        1. Tentukan indeks tengah mid = (first + last) // 2.
        2. Urutkan arr[first], arr[mid], arr[last] sehingga median ada di arr[first].
           (Kita pakai arr[first] sebagai pivot agar logika partitionSeq standar berlaku)
        3. Jalankan partisi Lomuto/Hoare standar dari arr[first+1] ke arr[last].

        Mengapa Median-of-Three lebih baik?
        - Pada data terurut terbalik (worst case pivot = elemen terkecil/terbesar),
          median-of-three akan memilih nilai tengah → partisi lebih seimbang.
        - Kompleksitas menjadi O(n log n) pada kebanyakan kasus praktis.

        Catatan stabilitas:
        Quick Sort inherently TIDAK stable karena swap jarak jauh bisa mengubah
        urutan relatif elemen bernilai sama. Untuk kebutuhan stable sort, gunakan
        sort_array() (Merge Sort) sebagai gantinya.

        Returns:
            Indeks akhir pivot setelah partisi.
        """
        mid = (first + last) // 2

        # --- Median-of-Three: urutkan first, mid, last ---
        # Setelah blok ini: arr[first] <= arr[mid] <= arr[last]
        # lalu kita swap arr[mid] ke arr[first] agar median jadi pivot
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Sekarang arr[first] = min, arr[mid] = median, arr[last] = max
        # Gunakan median sebagai pivot, taruh di arr[first]
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]

        # --- Partisi standar (two-pointer scan) ---
        left = first + 1
        right = last

        done = False
        while not done:
            # Geser left ke kanan selama elemen <= pivot
            while left <= right and arr[left] <= pivot:
                left += 1
            # Geser right ke kiri selama elemen > pivot
            while left <= right and arr[right] > pivot:
                right -= 1

            if left > right:
                done = True
            else:
                arr[left], arr[right] = arr[right], arr[left]

        # Tempatkan pivot ke posisi akhirnya
        arr[first], arr[right] = arr[right], arr[first]

        return right  # indeks pivot


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def build_linked_list(values: List[int]) -> Optional[ListNode]:
    """Buat linked list dari Python list (helper untuk testing)."""
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for v in values[1:]:
        current.next = ListNode(v)
        current = current.next
    return head


def linked_list_to_list(head: Optional[ListNode]) -> List[int]:
    """Konversi linked list ke Python list (helper untuk testing)."""
    result = []
    current = head
    while current:
        result.append(current.data)
        current = current.next
    return result


# =============================================================================
# DEMO & TEST
# =============================================================================

if __name__ == "__main__":
    sorter = AdvancedSorter()

    print("=" * 60)
    print("1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)")
    print("=" * 60)

    test_cases = [
        [38, 27, 43, 3, 9, 82, 10],
        [5, 5, 3, 3, 1, 1],          # Uji stabilitas: duplikat
        [1],                          # Edge case: 1 elemen
        [],                           # Edge case: kosong
        [2, 1],                       # Edge case: 2 elemen
        list(range(10, 0, -1)),       # Terurut terbalik
    ]

    for tc in test_cases:
        original = tc[:]
        result = sorter.sort_array(tc)
        print(f"  Input : {original}")
        print(f"  Output: {result}")
        print()

    print("=" * 60)
    print("2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)")
    print("=" * 60)

    ll_tests = [
        [64, 25, 12, 22, 11],
        [3, 1, 4, 1, 5, 9, 2, 6],    # Duplikat
        [1],
        [2, 1],
    ]

    for tc in ll_tests:
        head = build_linked_list(tc)
        sorted_head = sorter.sort_linked_list(head)
        result = linked_list_to_list(sorted_head)
        print(f"  Input : {tc}")
        print(f"  Output: {result}")
        print()

    print("=" * 60)
    print("3. QUICK SORT (Median-of-Three + Depth Fallback)")
    print("=" * 60)

    qs_tests = [
        [38, 27, 43, 3, 9, 82, 10],
        list(range(20, 0, -1)),       # Worst case tanpa median-of-three
        [1, 2, 3, 4, 5, 6, 7, 8],    # Sudah terurut (worst case naif)
        [5, 5, 5, 5],                 # Semua sama
    ]

    for tc in qs_tests:
        original = tc[:]
        result = sorter.sort_array_quicksort(tc)
        print(f"  Input : {original}")
        print(f"  Output: {result}")
        print()
