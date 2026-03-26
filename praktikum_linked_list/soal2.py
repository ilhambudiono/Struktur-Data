# ============================================================
#  Tugas Praktikum - Struktur Data
#  Soal 2  : Big Integer ADT + Assignment Combo Operators
#  Deadline : Jumat, 27 Maret 2026
# ============================================================
#
#  Soal 2 meng-extend BigInteger dari Soal 1A (linked list)
#  dengan menambahkan assignment combo operators:
#  +=   -=   *=   //=  %=  **=
#  <<=  >>=  |=   &=   ^=
# ============================================================


# ── Salin class Node & BigInteger dari soal1a ──────────────

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

        if initValue.startswith('-'):
            self.negative = True
            initValue = initValue[1:]

        initValue = initValue.lstrip('0') or '0'

        for ch in initValue:
            node = Node(int(ch))
            node.next = self.head
            self.head = node

    def toString(self):
        digits = []
        curr = self.head
        while curr:
            digits.append(str(curr.digit))
            curr = curr.next
        result = ''.join(reversed(digits)) or '0'
        return ('-' + result) if self.negative and result != '0' else result

    def _to_int(self):
        return int(self.toString())

    @staticmethod
    def _from_int(value):
        return BigInteger(str(value))

    def comparable(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '<' : a < b, '<=': a <= b,
            '>' : a > b, '>=': a >= b,
            '==': a == b, '!=': a != b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return operations[op]

    def arithmetic(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '+': a+b, '-': a-b, '*': a*b,
            '//': a//b, '%': a%b, '**': a**b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return BigInteger._from_int(operations[op])

    def bitwise_ops(self, other, op):
        a = self._to_int()
        b = other._to_int()
        operations = {
            '|': a|b, '&': a&b, '^': a^b,
            '<<': a<<b, '>>': a>>b,
        }
        if op not in operations:
            raise ValueError(f"Operator '{op}' tidak dikenal.")
        return BigInteger._from_int(operations[op])


# ── Soal 2: Tambah Assignment Combo Operators ──────────────

class BigIntegerV2(BigInteger):
    """
    Extends BigInteger dengan assignment combo operators.

    Cara pakai:
        a = BigIntegerV2("100")
        b = BigIntegerV2("25")
        a.iassign(b, '+=')   # setara: a += b
        print(a.toString())  # 125
    """

    # Mapping operator assignment -> operator dasar
    ARITH_OPS = {
        '+=': '+', '-=': '-',   '*=': '*',
        '//=': '//', '%=': '%', '**=': '**',
    }
    BIT_OPS = {
        '<<=': '<<', '>>=': '>>',
        '|=': '|',   '&=': '&',  '^=': '^',
    }

    def iassign(self, other, op):
        """
        Lakukan operasi assignment combo, simpan hasilnya ke self.

        Parameter:
            other : BigIntegerV2 — operand kanan
            op    : str          — operator (misal '+=', '*=', '<<=', dst.)

        Return:
            self (setelah diperbarui)
        """
        # Pastikan other bertipe BigInteger
        if not isinstance(other, BigInteger):
            other = BigIntegerV2(str(other))

        if op in self.ARITH_OPS:
            result = self.arithmetic(other, self.ARITH_OPS[op])
        elif op in self.BIT_OPS:
            result = self.bitwise_ops(other, self.BIT_OPS[op])
        else:
            raise ValueError(f"Operator assignment '{op}' tidak dikenal.")

        # Update internal state self dengan hasil
        self.head = result.head
        self.negative = result.negative
        return self


# ==============================================================
# MAIN - Testing
# ==============================================================

if __name__ == "__main__":
    sep = "=" * 50

    print(sep)
    print("SOAL 2 - Assignment Combo Operators")
    print(sep)

    x = BigIntegerV2("100")
    y = BigIntegerV2("25")
    print(f"x = {x.toString()}, y = {y.toString()}")
    print()

    # Arithmetic assignment
    print("[Arithmetic Assignment]")
    x.iassign(y, '+=')
    print(f"x += y    -> x = {x.toString()}")    # 125

    x.iassign(y, '*=')
    print(f"x *= y    -> x = {x.toString()}")    # 3125

    x.iassign(y, '//=')
    print(f"x //= y   -> x = {x.toString()}")   # 125

    x.iassign(y, '-=')
    print(f"x -= y    -> x = {x.toString()}")    # 100

    x.iassign(y, '%=')
    print(f"x %= y    -> x = {x.toString()}")    # 0

    x = BigIntegerV2("2")
    x.iassign(BigIntegerV2("10"), '**=')
    print(f"2 **= 10  -> x = {x.toString()}")   # 1024

    print()

    # Bitwise assignment
    print("[Bitwise Assignment]")
    x = BigIntegerV2("256")
    print(f"x = {x.toString()}")

    x.iassign(BigIntegerV2("2"), '<<=')
    print(f"x <<= 2   -> x = {x.toString()}")   # 1024

    x.iassign(BigIntegerV2("2"), '>>=')
    print(f"x >>= 2   -> x = {x.toString()}")   # 256

    x.iassign(BigIntegerV2("255"), '|=')
    print(f"x |= 255  -> x = {x.toString()}")   # 511

    x.iassign(BigIntegerV2("255"), '&=')
    print(f"x &= 255  -> x = {x.toString()}")   # 255

    x.iassign(BigIntegerV2("255"), '^=')
    print(f"x ^= 255  -> x = {x.toString()}")   # 0

    print()
    print("Selesai!")
    print(sep)
