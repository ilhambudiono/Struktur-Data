# Jawaban Teori: Analisis & Desain Algoritma Sorting Lanjutan

## Soal a — Ruang & Distribusi Sort

### Mengapa Radix Sort standar melanggar batasan O(1) di Modul A?

Radix Sort konvensional menggunakan **array of 10 queues** (satu queue per digit 0–9).
Setiap queue secara dinamis menampung elemen yang sedang diproses per pass.

- Pada setiap pass, **semua n elemen** harus "diparkir" sementara di dalam salah satu dari 10 queue tersebut sebelum digabungkan kembali ke array utama.
- Ini berarti memori tambahan yang dialokasikan **sebanding dengan n elemen** (bukan O(1)).
- Selain itu, struktur queue itu sendiri memerlukan overhead pointer atau index array tambahan.
- **Kesimpulan:** Radix Sort standar memiliki extra space O(n + k) di mana k = jumlah bucket (10 untuk desimal), sehingga **melanggar batasan O(1)** pada Modul A.

---

### Bagaimana mekanisme `tmpArray` tunggal pada Improved Merge Sort menekan overhead?

**Versi berbasis slice** (naif):
```
_merge_sort(arr[0:mid])   → membuat list baru ukuran mid
_merge_sort(arr[mid:n])   → membuat list baru ukuran n-mid
```
Setiap level rekursi membuat sublist fisik baru. Total alokasi memori di semua level rekursi = O(n log n).

**Versi `tmpArray` tunggal** (Listing 12.2 & 12.4):
```python
tmp_array = [0] * len(arr)   # Alokasi SEKALI di awal
_rec_merge_sort(arr, first, last, tmp_array)
```
- `tmpArray` dialokasikan **satu kali saja** di awal, ukuran n.
- Setiap rekursi hanya meneruskan **referensi** ke `tmpArray` yang sama beserta indeks `first`, `mid`, `last`.
- Rekursi yang berbeda menggunakan **bagian indeks yang berbeda** dari `tmpArray` dan tidak pernah tumpang tindih (karena merge dilakukan setelah kedua rekursi selesai — post-order).
- **Hasilnya:** extra space tetap O(n), bukan O(n log n).

---

### Alternatif Radix Sort yang tetap O(1) space

Satu-satunya cara mendekati "in-place Radix Sort" adalah **American Flag Sort** (varian in-place Radix Sort):

**Cara kerja:**
1. Lakukan **dua pass** per digit: pass pertama hitung frekuensi (histogram), pass kedua lakukan pemindahan elemen secara in-place dengan swap.
2. Karena hanya menggunakan array hitungan berukuran 10 (untuk desimal) atau konstanta tertentu, overhead ruang = O(k) ≈ O(1) jika k konstan.

**Dampak terhadap kompleksitas waktu:**
- Keuntungan: tetap O(d × n) di mana d = jumlah digit.
- Kerugian: implementasi jauh lebih kompleks dan konstanta waktu aktualnya lebih besar karena banyak swap berulang. Stabilitas juga sulit dijaga.
- Pada praktiknya, untuk n = 10⁶ dengan constraint O(1) space, **In-Place Merge Sort atau Heap Sort lebih realistis** daripada mencoba membuat Radix Sort benar-benar O(1).

---

## Soal b — Linked List & Pointer Manipulation

### Bagaimana `_splitLinkedList()` menemukan titik tengah dalam satu traversal?

Teknik ini disebut **Fast-Slow Pointer** (atau Floyd's Tortoise and Hare):

```
Awal:   H → 1 → 2 → 3 → 4 → 5 → None
        ^                 ^
     slow(mid)         fast(cur)
```

- `midPoint` (slow): bergerak **1 langkah** per iterasi.
- `curNode` (fast): bergerak **2 langkah** per iterasi.
- Loop: `while curNode and curNode.next:`

**Mengapa hasilnya adalah titik tengah?**

Ketika `curNode` mencapai akhir list (setelah menempuh ~n langkah), `midPoint` sudah menempuh ~n/2 langkah → berada di posisi tengah.

Ini memanfaatkan **rasio kecepatan 1:2** tanpa perlu menghitung panjang list terlebih dahulu → satu traversal saja cukup, kompleksitas O(n).

Setelah loop:
```python
right_head = midPoint.next
midPoint.next = None    # Putus link → dua sublist terpisah
```

---

### Mengapa dummy node + tail reference bisa berjalan tanpa alokasi memori tambahan?

```python
dummy = ListNode(0)   # Sentinel: menghindari edge case head pertama
tail = dummy

while listA and listB:
    if listA.data <= listB.data:
        tail.next = listA   # Tidak buat node baru, hanya ubah pointer
        listA = listA.next
    else:
        tail.next = listB
        listB = listB.next
    tail = tail.next

tail.next = listA or listB  # Sambung sisa
```

**Mengapa tidak ada alokasi baru?**
- Kita hanya **memodifikasi pointer `.next`** dari node-node yang sudah ada.
- Node `dummy` adalah satu-satunya alokasi, digunakan sebagai titik awal untuk menghindari logika khusus "node pertama belum ada".
- Semua node dari `listA` dan `listB` dirangkai ulang tanpa memindahkan data.

**Mengapa kompleksitas ruang O(log n)?**
- Per-merge call: O(1) — hanya variabel `dummy`, `tail`, dan pointer loop.
- Namun `sort_linked_list` memanggil dirinya sendiri secara rekursif sebanyak O(log n) level (karena list dibagi dua setiap kali).
- **Total ruang = O(log n)** berasal dari stack rekursi, bukan dari operasi merge itu sendiri.

---

## Soal c — Quick Sort Worst-Case & Pivot Strategy

### Mengapa data terurut terbalik menyebabkan kedalaman rekursi O(n) dan waktu O(n²)?

Pada Quick Sort naif (pivot = elemen pertama), untuk data `[5, 4, 3, 2, 1]`:

**Proses partisi `partitionSeq()`:**
- `left` dimulai dari `first+1`, bergerak ke kanan selama `arr[left] <= pivot`.
- `right` dimulai dari `last`, bergerak ke kiri selama `arr[right] > pivot`.
- Pivot = `arr[first]` = 5 (elemen terbesar).
- `left` tidak bisa bergerak karena semua elemen < pivot.
- `right` bergerak sampai `right == first`.
- Pivot ditempatkan di `first` kembali → **partisi menghasilkan sublist kosong (0 elemen) dan sublist n-1 elemen**.

**Dampak:**
```
Level 1: partisi [5,4,3,2,1] → [4,3,2,1] + [5]   (kedalaman +1)
Level 2: partisi [4,3,2,1]   → [3,2,1]   + [4]   (kedalaman +1)
...
Level n: [1]                                       (kedalaman n)
```
- Kedalaman rekursi = O(n) (bukan O(log n) seperti kasus rata-rata).
- Jumlah perbandingan total = n + (n-1) + ... + 1 = **O(n²)**.

---

### Strategi pivot yang lebih robust: Median-of-Three

**Cara kerja:**
1. Hitung `mid = (first + last) // 2`.
2. Bandingkan `arr[first]`, `arr[mid]`, `arr[last]`.
3. Pilih **nilai median** dari ketiganya sebagai pivot.
4. Swap median ke `arr[first]` sebelum partisi.

**Mengapa lebih baik?**
Pada data terurut terbalik `[5,4,3,2,1]`:
- `arr[first]=5`, `arr[mid]=3`, `arr[last]=1` → median = **3**.
- Pivot 3 membagi array menjadi dua bagian yang lebih seimbang: `[1,2]` dan `[4,5]`.
- Kedalaman rekursi menjadi O(log n), bukan O(n).

---

### Kelayakan Median-of-Three pada Singly Linked List

**Masalah utama:** Singly Linked List tidak mendukung akses acak.
- Mengakses `arr[mid]` pada array = O(1).
- Mengakses node tengah pada linked list = O(n) traversal.
- Mengakses node terakhir = O(n) traversal lagi.
- Total untuk memilih satu pivot median-of-three = **O(n)** — mahal!

**Kesimpulan:** Untuk linked list, strategi yang lebih realistis adalah:
1. Tetap gunakan **pivot elemen pertama** (O(1) akses).
2. Kombinasikan dengan **depth limiter**: jika kedalaman > 2 log n, fallback ke Merge Sort.
3. Atau gunakan **Merge Sort langsung** (jauh lebih cocok untuk linked list karena tidak memerlukan akses acak).

---

## Soal d — Batas Teoretis & Paradigma Sorting

### Mengapa Radix Sort O(dn) tidak kontradiktif dengan lower bound Ω(n log n)?

**Lower bound Ω(n log n)** hanya berlaku untuk **comparison-based sorting** — algoritma yang menentukan urutan elemen **hanya melalui perbandingan** (`<`, `>`, `<=`).

Pembuktian menggunakan **decision tree**:
- Setiap permutasi dari n elemen adalah salah satu dari n! kemungkinan output.
- Setiap perbandingan membagi kemungkinan menjadi dua cabang (ya/tidak).
- Untuk meng-cover semua n! kemungkinan, pohon keputusan harus memiliki ketinggian ≥ log₂(n!) = Ω(n log n).

**Radix Sort bukan comparison sort.** Ia tidak membandingkan elemen secara langsung. Sebaliknya, ia menggunakan nilai digit/karakter untuk mendistribusikan elemen ke bucket. Karena tidak membangun decision tree berbasis perbandingan, **lower bound Ω(n log n) tidak berlaku**.

---

### Dua asumsi implisit yang membuat Radix Sort "melampaui" lower bound

**Asumsi 1: d (jumlah digit) adalah konstan atau kecil (d = O(log n / log k))**

Jika nilai maksimum kunci adalah M dan kita menggunakan basis k, maka d = log_k(M).
- Jika M = O(n^c) untuk suatu konstanta c, maka d = O(log n) → Radix Sort = O(n log n), tidak lebih cepat dari comparison sort.
- Radix Sort benar-benar lebih cepat hanya jika M = O(n) atau d adalah konstanta kecil (misalnya 32-bit integer dengan basis 256: d = 4).

**Asumsi 2: k (ukuran alfabet/basis) adalah konstan atau tidak terlalu besar**

- Jika menggunakan basis k terlalu besar (misalnya k = n), maka bucket array berukuran n → extra space O(n) dan overhead inisialisasi O(n) per pass masih acceptable.
- Tetapi jika k sangat besar, biaya membuat dan menginisialisasi bucket per pass bisa mendominasi.

**Mengapa asumsi ini membatasi keunggulan Radix Sort?**
- Jika kunci adalah string panjang arbitrer (d besar), Radix Sort menjadi O(dn) = O(n²) atau lebih buruk.
- Jika domain kunci sangat besar (misalnya floating point atau string Unicode), Radix Sort kurang praktis.
- Comparison sort seperti Merge Sort lebih general: tidak peduli tipe data selama ada relasi `<`.
