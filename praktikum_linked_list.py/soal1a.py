# ============================================================
#  Tugas Praktikum - Struktur Data
#  Soal 1A : Big Integer ADT menggunakan Singly Linked List
#  Deadline : Jumat, 27 Maret 2026
# ============================================================


class Node:
    """Satu simpul dalam linked list, menyimpan satu digit."""
    def __init__(self, digit):
        self.digit = digit
        self.next = None


class BigInteger:
    """
    Big Integer ADT menggunakan singly linked list.
    Digit disimpan dari least-significant (kanan) ke most-significant (kiri).
    Contoh: 45839 -> head -> [9] -> [3] -> [8] -> [5] -> [4] -> None
    """

    def __init__(self, initValue="0"):
        self.head = None
        self.negative = False

        # Tangani tanda negatif
        if initValue.startswith('-'):
            self.negative = True
            initValue = initValue[1:]

        # Hilangkan leading zeros (misal "0045" -> "45")
        initValue = initValue.lstrip('0') or '0'

        # Masukkan digit dari kanan ke kiri (least-significant di depan)
        for ch in initValue:
            node = Node(int(ch))
            node.next = self.head
            self.head = node

    # ----------------------------------------------------------
    # toString(): kembalikan representasi string
    # ----------------------------------------------------------
    def toString(self):
        digits = []
        curr = self.head
        while curr:
            digits.append(str(curr.digit))
            curr = curr.next
        result = ''.join(reversed(digits)) or '0'
        return ('-' + result) if self.negative and result != '0' else result

    # ----------------------------------------------------------
    # Helper internal
    # ----------------------------------------------------------
    def _to_int(self):
        return int(self.toString())

    @staticmethod
    def _from_int(value):
        return BigInteger(str(value))

    # ----------------------------------------------------------
    # comparable(other, op): bandingkan dua BigInteger
    # op yang tersedia: '<', '<=', '>', '>=', '==', '!='
    # ----------------------------------------------------------
    def comparable(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '<' : a < b,
            '<=': a <= b,
            '>' : a > b,
            '>=': a >= b,
            '==': a == b,
            '!=': a != b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return operations[op]

    # ----------------------------------------------------------
    # arithmetic(other, op): operasi aritmatika
    # op yang tersedia: '+', '-', '*', '//', '%', '**'
    # ----------------------------------------------------------
    def arithmetic(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '+' : a + b,
            '-' : a - b,
            '*' : a * b,
            '//': a // b,
            '%' : a % b,
            '**': a ** b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return BigInteger._from_int(operations[op])

    # ----------------------------------------------------------
    # bitwise_ops(other, op): operasi bitwise
    # op yang tersedia: '|', '&', '^', '<<', '>>'
    # ----------------------------------------------------------
    def bitwise_ops(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '|' : a | b,
            '&' : a & b,
            '^' : a ^ b,
            '<<': a << b,
            '>>': a >> b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return BigInteger._from_int(operations[op])


# ==============================================================
# MAIN - Testing
# ==============================================================

if __name__ == "__main__":
    sep = "=" * 50

    print(sep)
    print("SOAL 1A - BigInteger dengan Linked List")
    print(sep)

    a = BigInteger("45839")
    b = BigInteger("123")

    print(f"a = {a.toString()}")
    print(f"b = {b.toString()}")
    print()

    print("[Arithmetic]")
    print(f"a + b  = {a.arithmetic(b, '+').toString()}")
    print(f"a - b  = {a.arithmetic(b, '-').toString()}")
    print(f"a * b  = {a.arithmetic(b, '*').toString()}")
    print(f"a // b = {a.arithmetic(b, '//').toString()}")
    print(f"a % b  = {a.arithmetic(b, '%').toString()}")
    print(f"a ** b = {a.arithmetic(b, '**').toString()}")
    print()

    print("[Comparable]")
    print(f"a < b  : {a.comparable(b, '<')}")
    print(f"a > b  : {a.comparable(b, '>')}")
    print(f"a == b : {a.comparable(b, '==')}")
    print(f"a != b : {a.comparable(b, '!=')}")
    print()

    print("[Bitwise]")
    print(f"a | b  = {a.bitwise_ops(b, '|').toString()}")
    print(f"a & b  = {a.bitwise_ops(b, '&').toString()}")
    print(f"a ^ b  = {a.bitwise_ops(b, '^').toString()}")
    print(f"a << 2 = {a.bitwise_ops(BigInteger('2'), '<<').toString()}")
    print(f"a >> 2 = {a.bitwise_ops(BigInteger('2'), '>>').toString()}")

    print()
    print("Selesai!")
    print(sep)
