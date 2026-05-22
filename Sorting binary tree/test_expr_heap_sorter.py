"""
test_expr_heap_sorter.py
========================
Unit tests untuk modul expr_heap_sorter.py

Cara menjalankan:
    python test_expr_heap_sorter.py
    # atau jika ada pytest:
    pytest test_expr_heap_sorter.py -v
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from expr_heap_sorter import ExprHeapSorter


def assert_equal(actual, expected, test_name, tolerance=None):
    if tolerance is not None:
        ok = abs(actual - expected) <= tolerance
    else:
        ok = actual == expected
    if ok:
        print(f"  ✓ PASS  {test_name}")
    else:
        print(f"  ✗ FAIL  {test_name}")
        print(f"         Expected: {expected}")
        print(f"         Got:      {actual}")


def assert_raises(func, exc_type, test_name):
    try:
        func()
        print(f"  ✗ FAIL  {test_name} (tidak raise exception)")
    except exc_type as e:
        print(f"  ✓ PASS  {test_name} (raised: {e})")
    except Exception as e:
        print(f"  ✗ FAIL  {test_name} (wrong exception: {type(e).__name__}: {e})")


def eval_expr(expr_str):
    """Helper: tokenize, build, eval."""
    s = ExprHeapSorter(expr_str)
    tokens = s._tokenize(expr_str)
    root = s._build_tree(tokens)
    return s._eval_tree(root)


def test_expression_tree_basic():
    print("\n[1] Expression Tree Basic Tests")

    # Dari soal: ((8 * 5) + (9 / (7 - 4))) = 40 + 3 = 43
    assert_equal(eval_expr("((8 * 5) + (9 / (7 - 4)))"), 43.0, "Soal utama: 43", tolerance=1e-9)

    assert_equal(eval_expr("((3 + 4) * (2 - 1))"), 7.0, "(3+4)*(2-1) = 7", tolerance=1e-9)
    assert_equal(eval_expr("((10 / 2) + (3 * 4))"), 17.0, "(10/2)+(3*4) = 17", tolerance=1e-9)
    assert_equal(eval_expr("(5 + 3)"), 8.0, "(5+3) = 8", tolerance=1e-9)
    assert_equal(eval_expr("(10 - 3)"), 7.0, "(10-3) = 7", tolerance=1e-9)
    assert_equal(eval_expr("(6 / 2)"), 3.0, "(6/2) = 3", tolerance=1e-9)


def test_expression_tree_edge_cases():
    print("\n[2] Expression Tree Edge Cases")

    # Angka multi-digit
    assert_equal(eval_expr("(100 + 200)"), 300.0, "Multi-digit numbers: 100+200", tolerance=1e-9)
    assert_equal(eval_expr("((42 * 10) - 5)"), 415.0, "42*10-5 = 415", tolerance=1e-9)


def test_division_by_zero():
    print("\n[3] Division by Zero Handling")

    def div_zero():
        eval_expr("(8 / (4 - 4))")

    assert_raises(div_zero, ValueError, "Division by zero → ValueError")

    def div_zero2():
        eval_expr("(100 / (0))")

    assert_raises(div_zero2, ValueError, "Division by zero literal → ValueError")


def test_postfix_output():
    print("\n[4] Postfix (Postorder) Output Tests")

    s = ExprHeapSorter("")

    # ((8 * 5) + (9 / (7 - 4))) → postfix: 8 5 * 9 7 4 - / +
    expr = "((8 * 5) + (9 / (7 - 4)))"
    tokens = s._tokenize(expr)
    root = s._build_tree(tokens)
    tokens2 = s._tokenize(expr)
    root2 = s._build_tree(tokens2)
    postfix = s._postorder_string(root2)
    assert_equal(postfix, "8 5 * 9 7 4 - / +", "Postfix dari soal utama")

    # (3 + 4) → postfix: 3 4 +
    tokens3 = s._tokenize("(3 + 4)")
    root3 = s._build_tree(tokens3)
    tokens4 = s._tokenize("(3 + 4)")
    root4 = s._build_tree(tokens4)
    postfix2 = s._postorder_string(root4)
    assert_equal(postfix2, "3 4 +", "Postfix simple: 3 4 +")


def test_heapsort_basic():
    print("\n[5] Heapsort In-Place Basic Tests")
    s = ExprHeapSorter("")

    assert_equal(s.heapsort_inplace([38, 27, 43, 3, 9, 82, 10]),
                 [3, 9, 10, 27, 38, 43, 82],
                 "Normal array")

    assert_equal(s.heapsort_inplace([5, 4, 3, 2, 1]),
                 [1, 2, 3, 4, 5],
                 "Reverse sorted")

    assert_equal(s.heapsort_inplace([1, 2, 3, 4, 5]),
                 [1, 2, 3, 4, 5],
                 "Already sorted")

    assert_equal(s.heapsort_inplace([5, 5, 5, 5]),
                 [5, 5, 5, 5],
                 "All same")

    assert_equal(s.heapsort_inplace([1]),
                 [1],
                 "Single element")

    assert_equal(s.heapsort_inplace([]),
                 [],
                 "Empty")

    assert_equal(s.heapsort_inplace([100, 1, 50, 25, 75]),
                 [1, 25, 50, 75, 100],
                 "Mixed values")


def test_heapsort_duplicates():
    print("\n[6] Heapsort Duplicates Tests")
    s = ExprHeapSorter("")

    assert_equal(s.heapsort_inplace([3, 1, 4, 1, 5, 9, 2, 6, 5, 3]),
                 [1, 1, 2, 3, 3, 4, 5, 5, 6, 9],
                 "Array with duplicates")

    assert_equal(s.heapsort_inplace([5, 5, 3, 3, 1, 1]),
                 [1, 1, 3, 3, 5, 5],
                 "Pairs of duplicates")


def test_sift_down():
    print("\n[7] Sift-Down Tests")
    s = ExprHeapSorter("")

    # Setelah sift-down pada root, root harus berisi nilai terbesar
    arr = [1, 9, 3, 7, 5, 2, 8]
    s._sift_down(arr, len(arr), 0)
    assert_equal(arr[0], 9, "Root setelah sift-down = max element")

    # Heap order: arr[i] >= arr[2*i+1] dan arr[i] >= arr[2*i+2]
    def check_heap(arr, n):
        for i in range(n // 2):
            left = 2 * i + 1
            right = 2 * i + 2
            if left < n and arr[i] < arr[left]:
                return False
            if right < n and arr[i] < arr[right]:
                return False
        return True

    arr2 = [3, 1, 4, 1, 5, 9, 2, 6]
    n = len(arr2)
    for i in range(n // 2 - 1, -1, -1):
        s._sift_down(arr2, n, i)
    assert_equal(check_heap(arr2, n), True, "Build heap: heap order property satisfied")


def test_complete_tree_validator():
    print("\n[8] Complete Tree Validator Tests")
    s = ExprHeapSorter("")

    # Valid: complete trees
    assert_equal(s.is_complete_tree([1, 2, 3, 4, 5]), True,
                 "[1,2,3,4,5] → complete")
    assert_equal(s.is_complete_tree([1, 2, 3, 4, 5, 6, 7]), True,
                 "[1..7] → complete (full)")
    assert_equal(s.is_complete_tree([1, 2, 3]), True,
                 "[1,2,3] → complete")
    assert_equal(s.is_complete_tree([1]), True,
                 "[1] → complete")
    assert_equal(s.is_complete_tree([]), True,
                 "[] → complete (trivially)")
    assert_equal(s.is_complete_tree([1, 2, 3, 4, 5, 6]), True,
                 "[1..6] → complete")


def test_parse_and_evaluate_integration():
    print("\n[9] Integration: parse_and_evaluate")

    s = ExprHeapSorter("((8 * 5) + (9 / (7 - 4)))")
    result = s.parse_and_evaluate()
    assert_equal(len(result), 1, "Returns list with 1 element")
    assert_equal(result[0], 43, "Value = 43")

    # Bisa digunakan sebagai input heapsort
    data = [15, 3, 42, 8, 27, 1, 99, 11] + result
    s.heapsort_inplace(data)
    assert_equal(data, sorted([15, 3, 42, 8, 27, 1, 99, 11, 43]),
                 "Integration: parse + heapsort produces sorted array")


if __name__ == "__main__":
    print("=" * 55)
    print("  UNIT TESTS: ExprHeapSorter")
    print("=" * 55)

    test_expression_tree_basic()
    test_expression_tree_edge_cases()
    test_division_by_zero()
    test_postfix_output()
    test_heapsort_basic()
    test_heapsort_duplicates()
    test_sift_down()
    test_complete_tree_validator()
    test_parse_and_evaluate_integration()

    print("\n" + "=" * 55)
    print("  Semua test selesai dijalankan.")
    print("=" * 55)
