# ============================================================
#  Tugas Praktikum - Struktur Data
#  Soal 1B : Big Integer ADT menggunakan Python List
#  Deadline : Jumat, 27 Maret 2026
# ============================================================


class BigIntegerList:
    """
    Big Integer ADT menggunakan Python list.
    Digit disimpan dari least-significant ke most-significant.
    Contoh: 45839 -> [9, 3, 8, 5, 4]
    """

    def __init__(self, initValue="0"):
        self.negative = False

        # Tangani tanda negatif
        if initValue.startswith('-'):
            self.negative = True
            initValue = initValue[1:]

        # Hilangkan leading zeros
        initValue = initValue.lstrip('0') or '0'

        # Simpan digit dari kanan ke kiri
        self.digits = [int(ch) for ch in reversed(initValue)]

    # ----------------------------------------------------------
    # toString(): kembalikan representasi string
    # ----------------------------------------------------------
    def toString(self):
        result = ''.join(str(d) for d in reversed(self.digits)) or '0'
        return ('-' + result) if self.negative and result != '0' else result

    # ----------------------------------------------------------
    # Helper internal
    # ----------------------------------------------------------
    def _to_int(self):
        return int(self.toString())

    @staticmethod
    def _from_int(value):
        return BigIntegerList(str(value))

    # ----------------------------------------------------------
    # comparable(other, op): bandingkan dua BigIntegerList
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
        return BigIntegerList._from_int(operations[op])

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
        return BigIntegerList._from_int(operations[op])


# ==============================================================
# MAIN - Testing
# ==============================================================

if __name__ == "__main__":
    sep = "=" * 50

    print(sep)
    print("SOAL 1B - BigInteger dengan Python List")
    print(sep)

    c = BigIntegerList("45839")
    d = BigIntegerList("123")

    print(f"c = {c.toString()}")
    print(f"d = {d.toString()}")
    print()

    print("[Arithmetic]")
    print(f"c + d  = {c.arithmetic(d, '+').toString()}")
    print(f"c - d  = {c.arithmetic(d, '-').toString()}")
    print(f"c * d  = {c.arithmetic(d, '*').toString()}")
    print(f"c // d = {c.arithmetic(d, '//').toString()}")
    print(f"c % d  = {c.arithmetic(d, '%').toString()}")
    print(f"c ** d = {c.arithmetic(d, '**').toString()}")
    print()

    print("[Comparable]")
    print(f"c < d  : {c.comparable(d, '<')}")
    print(f"c > d  : {c.comparable(d, '>')}")
    print(f"c == d : {c.comparable(d, '==')}")
    print(f"c != d : {c.comparable(d, '!=')}")
    print()

    print("[Bitwise]")
    print(f"c | d  = {c.bitwise_ops(d, '|').toString()}")
    print(f"c & d  = {c.bitwise_ops(d, '&').toString()}")
    print(f"c ^ d  = {c.bitwise_ops(d, '^').toString()}")
    print(f"c << 2 = {c.bitwise_ops(BigIntegerList('2'), '<<').toString()}")
    print(f"c >> 2 = {c.bitwise_ops(BigIntegerList('2'), '>>').toString()}")

    print()
    print("Selesai!")
    print(sep)
