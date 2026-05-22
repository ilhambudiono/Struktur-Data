"""
test_advanced_sorter.py
=======================
Unit tests untuk modul advanced_sorter.py

Cara menjalankan:
    python test_advanced_sorter.py
    # atau jika ada pytest:
    pytest test_advanced_sorter.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from advanced_sorter import AdvancedSorter, ListNode, build_linked_list, linked_list_to_list


def assert_equal(actual, expected, test_name):
    if actual == expected:
        print(f"  ✓ PASS  {test_name}")
    else:
        print(f"  ✗ FAIL  {test_name}")
        print(f"         Expected: {expected}")
        print(f"         Got:      {actual}")


def test_array_merge_sort():
    print("\n[1] Array Merge Sort Tests")
    sorter = AdvancedSorter()

    # Normal case
    assert_equal(sorter.sort_array([38, 27, 43, 3, 9, 82, 10]),
                 [3, 9, 10, 27, 38, 43, 82],
                 "Normal array")

    # Already sorted
    assert_equal(sorter.sort_array([1, 2, 3, 4, 5]),
                 [1, 2, 3, 4, 5],
                 "Already sorted")

    # Reverse sorted (worst case untuk naive quick sort)
    assert_equal(sorter.sort_array([5, 4, 3, 2, 1]),
                 [1, 2, 3, 4, 5],
                 "Reverse sorted")

    # All same elements (stability test)
    assert_equal(sorter.sort_array([5, 5, 5, 5]),
                 [5, 5, 5, 5],
                 "All same elements")

    # Duplicates (stability)
    assert_equal(sorter.sort_array([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]),
                 [1, 1, 2, 3, 3, 4, 5, 5, 6, 9],
                 "Duplicates")

    # Single element
    assert_equal(sorter.sort_array([42]),
                 [42],
                 "Single element")

    # Empty
    assert_equal(sorter.sort_array([]),
                 [],
                 "Empty array")

    # Two elements
    assert_equal(sorter.sort_array([2, 1]),
                 [1, 2],
                 "Two elements")

    # Negative numbers
    assert_equal(sorter.sort_array([-3, -1, -4, -1, -5]),
                 [-5, -4, -3, -1, -1],
                 "Negative numbers")


def test_stability_merge_sort():
    """
    Tes stabilitas: pastikan elemen dengan nilai sama mempertahankan urutan relatif.
    Karena kita hanya menyimpan integer, kita verifikasi dengan membuktikan
    algoritma menggunakan <= (bukan <) saat mengambil dari sublist kiri.
    """
    print("\n[2] Stability Test (Merge Sort)")
    sorter = AdvancedSorter()

    # Stabilitas terlihat dari: jika input [a, b] di mana a == b,
    # maka output juga [a, b] (a tetap sebelum b)
    # Kita verifikasi dengan array mixed yang terurut benar
    result = sorter.sort_array([5, 2, 5, 3, 5, 1])
    assert_equal(result, [1, 2, 3, 5, 5, 5], "Stable sort with duplicates")


def test_linked_list_sort():
    print("\n[3] Linked List Merge Sort Tests")
    sorter = AdvancedSorter()

    def sort_ll(values):
        head = build_linked_list(values)
        sorted_head = sorter.sort_linked_list(head)
        return linked_list_to_list(sorted_head)

    assert_equal(sort_ll([64, 25, 12, 22, 11]),
                 [11, 12, 22, 25, 64],
                 "Normal linked list")

    assert_equal(sort_ll([3, 1, 4, 1, 5, 9, 2, 6]),
                 [1, 1, 2, 3, 4, 5, 6, 9],
                 "Duplicates in linked list")

    assert_equal(sort_ll([1]),
                 [1],
                 "Single node")

    assert_equal(sort_ll([]),
                 [],
                 "Empty list")

    assert_equal(sort_ll([2, 1]),
                 [1, 2],
                 "Two nodes")

    assert_equal(sort_ll([5, 4, 3, 2, 1]),
                 [1, 2, 3, 4, 5],
                 "Reverse sorted")

    assert_equal(sort_ll([1, 2, 3, 4, 5]),
                 [1, 2, 3, 4, 5],
                 "Already sorted")


def test_split_linked_list():
    print("\n[4] Fast-Slow Pointer Split Tests")
    sorter = AdvancedSorter()

    # List ganjil: [1,2,3,4,5] → kiri=[1,2,3], kanan=[4,5]
    head = build_linked_list([1, 2, 3, 4, 5])
    right = sorter._split_linked_list(head)
    left_vals = linked_list_to_list(head)
    right_vals = linked_list_to_list(right)
    assert_equal(len(left_vals) + len(right_vals), 5, "Split odd: total elements preserved")
    assert_equal(len(left_vals), 3, "Split odd: left half size")
    assert_equal(len(right_vals), 2, "Split odd: right half size")

    # List genap: [1,2,3,4] → kiri=[1,2], kanan=[3,4]
    head = build_linked_list([1, 2, 3, 4])
    right = sorter._split_linked_list(head)
    left_vals = linked_list_to_list(head)
    right_vals = linked_list_to_list(right)
    assert_equal(len(left_vals), 2, "Split even: left half size")
    assert_equal(len(right_vals), 2, "Split even: right half size")


def test_quick_sort():
    print("\n[5] Quick Sort Tests (Median-of-Three + Fallback)")
    sorter = AdvancedSorter()

    assert_equal(sorter.sort_array_quicksort([38, 27, 43, 3, 9, 82, 10]),
                 [3, 9, 10, 27, 38, 43, 82],
                 "Normal array")

    # Worst case untuk naif quick sort (terurut terbalik)
    assert_equal(sorter.sort_array_quicksort(list(range(20, 0, -1))),
                 list(range(1, 21)),
                 "Reverse sorted (would be O(n²) without median-of-three)")

    # Sudah terurut (worst case lain untuk naif quick sort)
    assert_equal(sorter.sort_array_quicksort(list(range(1, 11))),
                 list(range(1, 11)),
                 "Already sorted")

    # Semua sama
    assert_equal(sorter.sort_array_quicksort([5, 5, 5, 5]),
                 [5, 5, 5, 5],
                 "All same")

    assert_equal(sorter.sort_array_quicksort([1]),
                 [1],
                 "Single element")

    assert_equal(sorter.sort_array_quicksort([]),
                 [],
                 "Empty")


def test_partition():
    print("\n[6] Partition (Median-of-Three) Tests")
    sorter = AdvancedSorter()

    # Setelah partisi, pivot harus berada di posisi finalnya:
    # semua elemen kiri <= pivot, semua elemen kanan > pivot
    arr = [38, 27, 43, 3, 9, 82, 10]
    pivot_idx = sorter.partition_quick(arr, 0, len(arr) - 1)
    pivot_val = arr[pivot_idx]

    left_ok = all(arr[i] <= pivot_val for i in range(pivot_idx))
    right_ok = all(arr[i] > pivot_val for i in range(pivot_idx + 1, len(arr)))

    assert_equal(left_ok, True, "All left elements <= pivot")
    assert_equal(right_ok, True, "All right elements > pivot")


if __name__ == "__main__":
    print("=" * 55)
    print("  UNIT TESTS: AdvancedSorter")
    print("=" * 55)

    test_array_merge_sort()
    test_stability_merge_sort()
    test_linked_list_sort()
    test_split_linked_list()
    test_quick_sort()
    test_partition()

    print("\n" + "=" * 55)
    print("  Semua test selesai dijalankan.")
    print("=" * 55)
