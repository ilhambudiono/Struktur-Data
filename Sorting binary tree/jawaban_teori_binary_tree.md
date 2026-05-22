# Jawaban Teori: Teori & Analisis Algoritma Binary Tree

## Soal a — Pohon Ekspresi & Traversal

### Langkah-langkah `_buildTree()` membangun pohon ekspresi dari `((8 * 5) + (9 / (7 - 4)))`

Token setelah tokenisasi (antrian dari kiri ke kanan):
```
( ( 8 * 5 ) + ( 9 / ( 7 - 4 ) ) )
```

**Penelusuran rekursi:**

```
_buildTree() dipanggil pertama kali:
  Ambil '(' → ini sub-ekspresi
  └─ Rekursi KIRI:
       Ambil '(' → sub-ekspresi
       └─ Rekursi KIRI:  Ambil '8' → leaf node {val:8}
          Ambil '*'       → operator
          Rekursi KANAN: Ambil '5' → leaf node {val:5}
          Ambil ')'       → tutup sub-ekspresi
          Kembalikan {val:'*', left:{8}, right:{5}}
  Ambil '+' → operator root
  └─ Rekursi KANAN:
       Ambil '(' → sub-ekspresi
       └─ Rekursi KIRI:  Ambil '9' → leaf node {val:9}
          Ambil '/'       → operator
          Rekursi KANAN:
            Ambil '(' → sub-ekspresi
            └─ Rekursi KIRI:  Ambil '7' → leaf node {val:7}
               Ambil '-'       → operator
               Rekursi KANAN: Ambil '4' → leaf node {val:4}
               Ambil ')'       → tutup
               Kembalikan {val:'-', left:{7}, right:{4}}
          Ambil ')'       → tutup
          Kembalikan {val:'/', left:{9}, right:{'-'}}
  Ambil ')' → tutup root
  Kembalikan {val:'+', left:{'*'}, right:{'/'}}
```

**Pohon yang terbentuk:**
```
           +
         /   \
        *     /
       / \   / \
      8   5 9   -
               / \
              7   4
```

---

### Mengapa postorder menghasilkan notasi postfix yang valid secara otomatis?

**Traversal Postorder:** kiri → kanan → root

Untuk pohon di atas:
```
Postorder: 8  5  *  9  7  4  -  /  +
```
Ini adalah notasi postfix `8 5 * 9 7 4 - / +` yang valid, karena:
- Setiap operator muncul **setelah** kedua operandnya → mesin stack dapat langsung mengevaluasi tanpa perlu melihat ke depan.
- Urutan evaluasi sudah **tersimpan implisit** dalam struktur pohon.

**Mengapa inorder memerlukan tanda kurung eksplisit?**

Traversal Inorder: kiri → root → kanan

Menghasilkan: `8 * 5 + 9 / 7 - 4`

Tanpa tanda kurung, ini ambigu:
- Apakah `(8*5) + (9/(7-4))` atau `8*(5+9)/(7-4)`?
- Operator seperti `+` dan `/` memiliki **prioritas berbeda**, dan inorder tidak menyimpan informasi ini.
- Sehingga Listing 13.7 perlu menambahkan `(` dan `)` secara eksplisit untuk mengembalikan makna yang benar.

---

### Kedalaman maksimum stack rekursi untuk `_buildString()` dengan tinggi pohon h

Fungsi `_buildString()` (yang menghasilkan representasi string dari pohon) memanggil dirinya sendiri secara rekursif untuk subtree kiri dan kanan.

- Kedalaman rekursi maksimum = **tinggi pohon h**.
- Untuk pohon dengan tinggi h, stack rekursi akan menampung maksimum **h + 1 frame** secara bersamaan (satu per level dari root ke leaf terdalam).
- **Kompleksitas ruang stack = O(h)**.

Untuk pohon yang seimbang dengan n node: h = O(log n) → stack O(log n).
Untuk pohon yang degenerasi (satu rantai): h = O(n) → stack O(n).

---

## Soal b — Struktur Heap & Pemetaan Array

### Mengapa rumus indeks valid hanya untuk Complete Binary Tree?

Rumus:
- Parent dari node i: `(i - 1) // 2`
- Anak kiri node i: `2*i + 1`
- Anak kanan node i: `2*i + 2`

Rumus ini bekerja karena **Complete Binary Tree** memiliki sifat:
- Level 0 (root): 1 node → indeks 0
- Level 1: 2 node → indeks 1, 2
- Level 2: 4 node → indeks 3, 4, 5, 6
- dst.

Pengisian dilakukan **dari kiri ke kanan, level per level** (BFS order), sehingga tidak ada "lubang" (gap) dalam pemetaan indeks.

Jika pohon bukan complete (ada lubang), misalnya node di indeks 1 ada tetapi indeks 2 tidak ada, maka:
- Anak kiri dari node 1 = 3 → ada di array
- Anak kiri dari node 2 = 5 → ada di array, padahal node 2 tidak ada!
- **Rumus aritmetika jadi tidak bermakna** karena tidak mencerminkan struktur pohon yang sebenarnya.

---

### Bagaimana `sift-down()` memulihkan heap order setelah ekstraksi akar?

**Situasi awal:** root (maksimum) di-extract → posisi root diisi dengan elemen terakhir array (yang mungkin kecil).

**Langkah sift-down:**
```
1. idx = 0 (root yang baru, mungkin nilainya kecil)
2. Hitung left = 2*0+1 = 1, right = 2*0+2 = 2
3. Cari largest di antara arr[idx], arr[left], arr[right]
4. Jika largest != idx → swap arr[idx] dengan arr[largest]
5. idx = largest, ulangi dari langkah 2
6. Berhenti jika largest == idx (sudah di posisi tepat)
```

Proses ini mendorong elemen kecil **turun ke level yang sesuai** sambil mengangkat elemen yang lebih besar ke atas → heap order property terpulihkan.

---

### Jumlah perbandingan maksimum satu sift-down untuk heap ukuran n

- Tinggi heap h = ⌊log₂(n)⌋
- Setiap level memerlukan **2 perbandingan**: `arr[idx] vs arr[left]` dan kemudian `vs arr[right]` (atau cukup mencari `largest`).
- Sift-down paling jauh turun h level.

**Maksimum perbandingan = 2 × ⌊log₂(n)⌋ = O(log n)**

Contoh untuk n = 7 (h = 2): maksimum 4 perbandingan per sift-down call.

---

## Soal c — Heapsort In-Place vs Simple

### Perbandingan Simple Heapsort vs In-Place Heapsort

| Aspek | Simple Heapsort | In-Place Heapsort |
|-------|----------------|-------------------|
| **Kompleksitas Ruang Tambahan** | O(n) — membuat heap baru sebagai array terpisah, lalu menyalin kembali | O(1) — hanya variabel indeks; seluruh operasi dilakukan pada array input |
| **Pola Akses Memori** | Lebih cache-friendly di fase build (akses sekuensial ke array heap baru), tetapi ekstraksi ke array output menambah satu level indirection | Kurang cache-friendly: sift-down loncat antara parent dan child (indeks 2x lebih besar), sehingga akses memori lebih "acak". Cache miss lebih sering, terutama untuk heap besar. |
| **Risiko Overflow RAM Terbatas** | Tinggi: membutuhkan array tambahan berukuran n. Untuk n = 10⁶ integer (4 byte), perlu ~4 MB tambahan | Rendah: tidak ada alokasi memori dinamis selama sorting. Aman untuk embedded system dengan RAM terbatas |

---

### Mengapa In-Place Heapsort tetap O(n log n) meski swap berulang?

Dua fase heapsort in-place:

**Fase 1 – Build Max-Heap:** O(n)
- Meski terlihat O(n log n) (karena n/2 node × O(log n) sift-down), analisis amortized membuktikan O(n).
- Node di level bawah melakukan sift-down pendek (atau tidak sama sekali), dan node tersebut jauh lebih banyak daripada node di puncak.

**Fase 2 – Ekstraksi:** O(n log n)
- n-1 kali swap root ke akhir.
- Setiap sift-down = O(log n) karena tinggi heap berkurang 1 per iterasi.
- Total: Σ(i=1 ke n-1) O(log i) = O(n log n).

Swap yang "berulang" tidak menambah kompleksitas karena setiap swap hanya melibatkan **indeks yang dikomputasi secara aritmetika** (bukan traversal), dan jumlah total swap dibatasi oleh ketinggian heap yang terus mengecil.

---

## Soal d — Batas Teoretis & Decision Tree

### Mengapa Heapsort tidak melanggar lower bound Ω(n log n)?

Heapsort **adalah** comparison-based sort. Setiap keputusan (apakah `arr[left] > arr[idx]?`) adalah perbandingan dua elemen.

Lower bound Ω(n log n) berlaku untuk semua comparison sort. Heapsort tidak melanggarnya karena:
- Fase build-heap: O(n) perbandingan (lebih sedikit dari Ω(n log n), ini bukan sorting).
- Fase ekstraksi: O(n log n) perbandingan (ini yang melakukan sorting).
- **Total: O(n log n)** — tepat memenuhi lower bound, tidak melanggar.

Heapsort "memanfaatkan struktur pohon" hanya untuk **mempercepat pencarian elemen maksimum** (O(log n) per ekstraksi vs O(n) pada selection sort), bukan untuk menghindari keharusan membandingkan elemen.

---

### Properti null link untuk mendeteksi urutan token tidak valid pada Decision Tree Morse Code

Pohon keputusan Morse Code:
```
        root
       /    \
      .      -
     / \    / \
    ..  .-  -.  --
```
- Setiap edge kiri = `.` (titik), kanan = `-` (strip).
- Setiap node menyimpan karakter yang dikodekan oleh path dari root ke node tersebut.
- **Null link** = anak yang tidak ada (path yang tidak valid dalam kode Morse).

Cara deteksi urutan tidak valid:
1. Mulai dari root, traversal mengikuti token (`.` atau `-`).
2. Jika pada suatu titik, link yang harus diikuti adalah `null` (node tidak ada) → **urutan tidak valid**.
3. Jika traversal selesai tapi node saat ini tidak memiliki karakter → **kode tidak valid** (jarang terjadi jika pohon lengkap).

---

### Mengapa rekursif lebih cocok daripada iteratif untuk membangun pohon keputusan?

**Alasan utama:**

1. **Struktur data rekursif:** Pohon secara alami didefinisikan secara rekursif ("sebuah pohon adalah node dengan dua subtree yang masing-masing juga merupakan pohon"). Rekursi mengikuti definisi ini secara langsung.

2. **Kode lebih bersih:** Fungsi rekursif untuk bangun/traversal pohon biasanya 3–10 baris; versi iteratifnya memerlukan stack eksplisit dan lebih sulit dibaca.

3. **Tidak perlu stack manual:** Rekursi memanfaatkan call stack sistem untuk menyimpan "posisi saat ini" di pohon. Versi iteratif harus mengelola stack sendiri — sama kompleksitasnya tetapi lebih verbose.

4. **Kemudahan insersi:** Saat membangun pohon keputusan Morse Code, kita mengikuti path karakter demi karakter dan membuat node baru jika belum ada. Rekursi secara natural merepresentasikan "ikuti satu langkah, lalu rekursi untuk langkah berikutnya".

**Kapan iteratif lebih baik?** Hanya jika pohon sangat dalam (risiko stack overflow) atau pada sistem embedded tanpa dukungan rekursi yang memadai.
