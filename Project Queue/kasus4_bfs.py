"""
kasus4_bfs.py — BFS (Breadth-First Search)
============================================
Queue memastikan eksplorasi level demi level dari node awal.
Menjamin jalur terpendek pada graf tanpa bobot.

Algoritma:
  1. Enqueue node awal, tandai sebagai visited.
  2. Selama queue tidak kosong:
     a. Dequeue node terdepan.
     b. Proses node tersebut.
     c. Enqueue semua tetangga yang belum dikunjungi.
"""

from queue import Queue
from collections import defaultdict


def bfs(graph: dict, start: str, verbose: bool = True) -> list[str]:
    """
    BFS standar — kembalikan urutan kunjungan node.

    Parameters
    ----------
    graph   : adjacency list  {node: [tetangga, ...]}
    start   : node awal
    verbose : cetak log tiap langkah

    Returns
    -------
    Urutan node yang dikunjungi (list)
    """
    visited = set()
    queue = Queue(max_size=len(graph) + 1)
    urutan = []

    queue.enqueue(start)
    visited.add(start)

    if verbose:
        print(f"  Start  : {start}")
        print(f"  {'Queue':<30} {'Node diproses':<15} {'Enqueue'}")
        print("  " + "-" * 60)

    while not queue.is_empty():
        node = queue.dequeue()
        urutan.append(node)

        tetangga_baru = []
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
                tetangga_baru.append(neighbor)

        if verbose:
            isi_queue = [
                queue._data[(queue._front + i) % queue._max_size]
                for i in range(len(queue))
            ]
            print(f"  {str(isi_queue):<30} {node:<15} {tetangga_baru}")

    return urutan


def bfs_jalur_terpendek(graph: dict, start: str, end: str) -> list[str] | None:
    """
    BFS untuk menemukan jalur terpendek antara dua node.

    Returns
    -------
    Jalur sebagai list node, atau None jika tidak ada jalur.
    """
    if start == end:
        return [start]

    visited = set([start])
    queue = Queue(max_size=len(graph) + 1)
    queue.enqueue([start])           # simpan path, bukan hanya node

    while not queue.is_empty():
        path = queue.dequeue()
        node = path[-1]

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                new_path = path + [neighbor]
                if neighbor == end:
                    return new_path
                visited.add(neighbor)
                queue.enqueue(new_path)

    return None   # tidak ada jalur


def bfs_level(graph: dict, start: str) -> dict[str, int]:
    """
    BFS — kembalikan jarak (jumlah edge) tiap node dari start.
    """
    distances = {start: 0}
    queue = Queue(max_size=len(graph) + 1)
    queue.enqueue(start)

    while not queue.is_empty():
        node = queue.dequeue()
        for neighbor in graph.get(node, []):
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.enqueue(neighbor)

    return distances


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  KASUS 4: BFS — Breadth-First Search")
    print("=" * 55)

    # Graf tidak berarah
    #   A — B — D — G
    #   |   |   |
    #   C — E — H
    #   |
    #   F
    graf = {
        "A": ["B", "C"],
        "B": ["A", "D", "E"],
        "C": ["A", "E", "F"],
        "D": ["B", "G"],
        "E": ["B", "C", "G", "H"],
        "F": ["C"],
        "G": ["D", "E"],
        "H": ["E"],
    }

    print("\n--- BFS dari node A ---")
    urutan = bfs(graf, "A")
    print(f"\n  Urutan kunjungan : {urutan}")

    print("\n--- Jalur terpendek A → H ---")
    jalur = bfs_jalur_terpendek(graf, "A", "H")
    print(f"  Jalur : {' → '.join(jalur)}")
    print(f"  Panjang : {len(jalur) - 1} edge")

    print("\n--- Jalur terpendek A → G ---")
    jalur = bfs_jalur_terpendek(graf, "A", "G")
    print(f"  Jalur : {' → '.join(jalur)}")
    print(f"  Panjang : {len(jalur) - 1} edge")

    print("\n--- Jarak semua node dari A ---")
    jarak = bfs_level(graf, "A")
    for node, d in sorted(jarak.items()):
        print(f"  A → {node} : {d} langkah")

    # Graf terputus
    print("\n--- Graf tidak terhubung (A→Z) ---")
    jalur = bfs_jalur_terpendek(graf, "A", "Z")
    print(f"  Jalur : {jalur}  (None = tidak ada)")
