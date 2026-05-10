"""
kasus5_bandara.py — Simulasi Loket Tiket Bandara
==================================================
Discrete event simulation untuk menghitung rata-rata waktu tunggu.

Komponen:
  - Queue antrian penumpang
  - Array agen loket
  - Penumpang tiba secara acak (prob = 1 / between_time)

3 aturan per tick waktu:
  R1: Jika penumpang tiba → enqueue
  R2: Jika agen free & queue tidak kosong → dequeue, mulai layani
  R3: Jika transaksi selesai → penumpang keluar, agen free

Insight dari materi:
  2 agen → avg wait ≈ 475 menit
  3 agen → avg wait ≈ 1.14 menit
"""

import random
from queue import Queue


class Penumpang:
    """Mewakili satu penumpang dalam simulasi."""

    def __init__(self, arrival_time: int):
        self.arrival_time = arrival_time

    def waktu_tunggu(self, start_service: int) -> int:
        return start_service - self.arrival_time

    def __repr__(self):
        return f"Penumpang(tiba={self.arrival_time})"


class AgenLoket:
    """Satu loket yang bisa melayani penumpang."""

    def __init__(self, agent_id: int):
        self.id = agent_id
        self.busy = False
        self._service_time_remaining = 0
        self._current_passenger: Penumpang | None = None

    def mulai_layani(self, penumpang: Penumpang, service_time: int):
        self.busy = True
        self._current_passenger = penumpang
        self._service_time_remaining = service_time

    def tick(self) -> Penumpang | None:
        """Proses 1 satuan waktu. Kembalikan penumpang jika sudah selesai."""
        if not self.busy:
            return None
        self._service_time_remaining -= 1
        if self._service_time_remaining <= 0:
            selesai = self._current_passenger
            self.busy = False
            self._current_passenger = None
            return selesai
        return None

    def __repr__(self):
        if self.busy:
            return (f"Agen-{self.id}[SIBUK, sisa={self._service_time_remaining}]")
        return f"Agen-{self.id}[FREE]"


def simulasi_bandara(
    num_minutes: int = 60,
    num_agents: int = 2,
    service_time: int = 3,
    between_time: int = 3,
    seed: int | None = 42,
    verbose: bool = True,
) -> dict:
    """
    Jalankan simulasi loket tiket bandara.

    Parameters
    ----------
    num_minutes   : lama simulasi (tick)
    num_agents    : jumlah loket/agen
    service_time  : waktu layanan per penumpang (tick)
    between_time  : rata-rata interval kedatangan (1/prob)
    seed          : random seed untuk hasil konsisten
    verbose       : cetak log per tick

    Returns
    -------
    dict berisi statistik simulasi
    """
    if seed is not None:
        random.seed(seed)

    queue: Queue = Queue(max_size=500)
    agents = [AgenLoket(i + 1) for i in range(num_agents)]

    total_wait = 0
    num_served = 0
    num_arrived = 0

    if verbose:
        header = f"{'Tick':>5} | {'Tiba':>5} | {'Antrian':>7} | {'Agen (status)':>30} | {'Selesai':>7}"
        print(f"\n  {header}")
        print("  " + "-" * len(header))

    for cur_time in range(1, num_minutes + 1):

        # R1: Kedatangan acak
        arrived_this_tick = False
        if random.random() < 1 / between_time:
            queue.enqueue(Penumpang(cur_time))
            num_arrived += 1
            arrived_this_tick = True

        # R3: Agen yang selesai → bebaskan
        selesai_tick = 0
        for agent in agents:
            done = agent.tick()
            if done:
                num_served += 1
                selesai_tick += 1

        # R2: Agen bebas ambil penumpang berikutnya
        for agent in agents:
            if not agent.busy and not queue.is_empty():
                next_pax: Penumpang = queue.dequeue()
                total_wait += next_pax.waktu_tunggu(cur_time)
                agent.mulai_layani(next_pax, service_time)

        if verbose and (cur_time <= 20 or cur_time % 10 == 0):
            status_agen = " | ".join(
                f"A{a.id}:{'S' if a.busy else 'F'}" for a in agents
            )
            print(f"  {cur_time:>5} | {'✓' if arrived_this_tick else '-':>5} | "
                  f"{len(queue):>7} | {status_agen:>30} | {selesai_tick:>7}")

    avg_wait = total_wait / num_served if num_served else 0

    return {
        "num_agents":  num_agents,
        "num_arrived": num_arrived,
        "num_served":  num_served,
        "avg_wait":    round(avg_wait, 2),
        "sisa_antrian": len(queue),
    }


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 60)
    print("  KASUS 5: Simulasi Loket Tiket Bandara")
    print("=" * 60)

    configs = [
        {"num_agents": 1, "label": "1 agen"},
        {"num_agents": 2, "label": "2 agen"},
        {"num_agents": 3, "label": "3 agen"},
    ]

    for cfg in configs:
        print(f"\n{'─'*60}")
        print(f"  Konfigurasi: {cfg['label']} | 60 menit | service=3 | between=3")
        hasil = simulasi_bandara(
            num_minutes=60,
            num_agents=cfg["num_agents"],
            service_time=3,
            between_time=3,
            seed=42,
            verbose=(cfg["num_agents"] == 2),  # log detail hanya untuk 2 agen
        )
        print(f"\n  ── Hasil ({cfg['label']}) ──")
        print(f"  Penumpang tiba    : {hasil['num_arrived']}")
        print(f"  Penumpang dilayani: {hasil['num_served']}")
        print(f"  Rata-rata tunggu  : {hasil['avg_wait']} tick")
        print(f"  Sisa antrian      : {hasil['sisa_antrian']}")

    # Perbandingan langsung (simulasi panjang, tanpa verbose)
    print(f"\n{'─'*60}")
    print("  Perbandingan avg wait — simulasi 500 menit")
    print(f"{'─'*60}")
    for n in range(1, 5):
        r = simulasi_bandara(num_minutes=500, num_agents=n, verbose=False, seed=99)
        bar = "█" * min(int(r["avg_wait"] * 2), 40)
        print(f"  {n} agen | avg wait = {r['avg_wait']:>7.2f} tick  {bar}")
