import tkinter as tk
from tkinter import ttk
import random
from collections import deque
import heapq

CELL = 30

class MazeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Labirin Random - Maze Solver")
        self.root.resizable(False, False)

        self.cols = 15
        self.rows = 15
        self.grid = []
        self.solving = False
        self.anim_id = None

        self._build_ui()
        self.new_maze()

    def _build_ui(self):
        ctrl = tk.Frame(self.root, padx=10, pady=8)
        ctrl.pack(fill="x")

        tk.Label(ctrl, text="Ukuran:").pack(side="left")
        self.size_var = tk.StringVar(value="15")
        size_cb = ttk.Combobox(ctrl, textvariable=self.size_var, width=10,
                               values=["10  (Kecil)", "15  (Sedang)", "20  (Besar)", "25  (XL)"],
                               state="readonly")
        size_cb.pack(side="left", padx=(2, 10))

        tk.Label(ctrl, text="Algoritma:").pack(side="left")
        self.algo_var = tk.StringVar(value="bfs")
        algo_cb = ttk.Combobox(ctrl, textvariable=self.algo_var, width=14,
                               values=["bfs  (BFS terpendek)", "dfs  (DFS eksplorasi)", "astar  (A* heuristik)"],
                               state="readonly")
        algo_cb.pack(side="left", padx=(2, 10))

        tk.Button(ctrl, text="Labirin Baru", bg="#185FA5", fg="white",
                  command=self.new_maze, padx=8).pack(side="left", padx=2)
        tk.Button(ctrl, text="Cari Jalan", command=self.solve_maze, padx=8).pack(side="left", padx=2)
        tk.Button(ctrl, text="Reset", command=self.reset_path, padx=8).pack(side="left", padx=2)

        self.canvas = tk.Canvas(self.root, bg="#F1EFE8", highlightthickness=0)
        self.canvas.pack()

        self.status_var = tk.StringVar(value="Klik 'Labirin Baru' untuk mulai!")
        tk.Label(self.root, textvariable=self.status_var, fg="#5F5E5A",
                 font=("Arial", 10), pady=6).pack()

        legend = tk.Frame(self.root, pady=4)
        legend.pack()
        for color, label in [("#1D9E75","Start"), ("#D85A30","End"),
                              ("#B5D4F4","Dieksplorasi"), ("#378ADD","Jalur")]:
            f = tk.Frame(legend)
            f.pack(side="left", padx=8)
            tk.Canvas(f, width=14, height=14, bg=color, highlightthickness=1,
                      highlightbackground="#aaa").pack(side="left", padx=(0,3))
            tk.Label(f, text=label, font=("Arial", 9)).pack(side="left")

    def _get_size(self):
        val = self.size_var.get()
        return int(val.strip().split()[0])

    def _get_algo(self):
        return self.algo_var.get().strip().split()[0]

    def new_maze(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        self.solving = False

        self.cols = self._get_size()
        self.rows = self.cols
        w = self.cols * CELL
        h = self.rows * CELL
        self.canvas.config(width=w, height=h)

        self.grid = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                row.append({"c": c, "r": r, "walls": [True, True, True, True], "visited": False})
            self.grid.append(row)

        self._generate()
        self.status_var.set("Labirin siap! Klik 'Cari Jalan' untuk solve.")

    def _cell(self, c, r):
        return self.grid[r][c]

    def _generate(self):
        start = self._cell(0, 0)
        start["visited"] = True
        stack = [start]

        while stack:
            cur = stack[-1]
            neighbors = self._unvisited_neighbors(cur)
            if not neighbors:
                stack.pop()
                continue
            nxt = random.choice(neighbors)
            self._remove_wall(cur, nxt)
            nxt["visited"] = True
            stack.append(nxt)

        for r in self.grid:
            for c in r:
                c["visited"] = False

        self._draw_all()

    def _unvisited_neighbors(self, cell):
        c, r = cell["c"], cell["r"]
        result = []
        for dc, dr in [(0,-1),(1,0),(0,1),(-1,0)]:
            nc, nr = c+dc, r+dr
            if 0 <= nc < self.cols and 0 <= nr < self.rows:
                n = self._cell(nc, nr)
                if not n["visited"]:
                    result.append(n)
        return result

    def _remove_wall(self, a, b):
        dc = b["c"] - a["c"]
        dr = b["r"] - a["r"]
        if dc == 1:  a["walls"][1] = False; b["walls"][3] = False
        elif dc == -1: a["walls"][3] = False; b["walls"][1] = False
        elif dr == 1:  a["walls"][2] = False; b["walls"][0] = False
        elif dr == -1: a["walls"][0] = False; b["walls"][2] = False

    def _neighbors(self, c, r):
        cell = self._cell(c, r)
        result = []
        for i, (dc, dr) in enumerate([(0,-1),(1,0),(0,1),(-1,0)]):
            if not cell["walls"][i]:
                nc, nr = c+dc, r+dr
                if 0 <= nc < self.cols and 0 <= nr < self.rows:
                    result.append((nc, nr))
        return result

    def _draw_all(self, explored=None, path=None):
        cv = self.canvas
        cv.delete("all")

        if explored:
            for (c, r) in explored:
                x, y = c*CELL, r*CELL
                cv.create_rectangle(x+1, y+1, x+CELL-1, y+CELL-1, fill="#B5D4F4", outline="")

        if path:
            for (c, r) in path:
                x, y = c*CELL, r*CELL
                cv.create_rectangle(x+1, y+1, x+CELL-1, y+CELL-1, fill="#378ADD", outline="")

        for row in self.grid:
            for cell in row:
                c, r = cell["c"], cell["r"]
                x, y = c*CELL, r*CELL
                if cell["walls"][0]: cv.create_line(x, y, x+CELL, y, fill="#2C2C2A", width=2)
                if cell["walls"][1]: cv.create_line(x+CELL, y, x+CELL, y+CELL, fill="#2C2C2A", width=2)
                if cell["walls"][2]: cv.create_line(x+CELL, y+CELL, x, y+CELL, fill="#2C2C2A", width=2)
                if cell["walls"][3]: cv.create_line(x, y+CELL, x, y, fill="#2C2C2A", width=2)

        r = CELL * 0.32
        for (gc, gr), color in [((0,0),"#1D9E75"), ((self.cols-1, self.rows-1),"#D85A30")]:
            cx, cy = gc*CELL + CELL//2, gr*CELL + CELL//2
            cv.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color, outline="")

    def reset_path(self):
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None
        self.solving = False
        self._draw_all()
        self.status_var.set("Reset. Klik 'Cari Jalan' lagi.")

    def solve_maze(self):
        if self.solving: return
        if self.anim_id:
            self.root.after_cancel(self.anim_id)
            self.anim_id = None

        self._draw_all()
        algo = self._get_algo()
        self.status_var.set("Mencari jalur...")
        self.root.update()

        start = (0, 0)
        end = (self.cols-1, self.rows-1)

        if algo == "bfs":
            result = self._bfs(start, end)
        elif algo == "dfs":
            result = self._dfs(start, end)
        else:
            result = self._astar(start, end)

        if not result:
            self.status_var.set("Jalur tidak ditemukan!")
            return

        explored, path = result
        self._animate(explored, path, algo.upper())

    def _bfs(self, start, end):
        queue = deque([start])
        prev = {start: None}
        order = []
        while queue:
            cur = queue.popleft()
            order.append(cur)
            if cur == end: break
            for n in self._neighbors(*cur):
                if n not in prev:
                    prev[n] = cur
                    queue.append(n)
        if end not in prev: return None
        path, c = [], end
        while c: path.insert(0, c); c = prev[c]
        return order, path

    def _dfs(self, start, end):
        stack = [start]
        prev = {start: None}
        order = []
        while stack:
            cur = stack.pop()
            if cur in order: continue
            order.append(cur)
            if cur == end: break
            for n in self._neighbors(*cur):
                if n not in prev:
                    prev[n] = cur
                    stack.append(n)
        if end not in prev: return None
        path, c = [], end
        while c: path.insert(0, c); c = prev[c]
        return order, path

    def _astar(self, start, end):
        def h(pos): return abs(pos[0]-end[0]) + abs(pos[1]-end[1])
        open_heap = [(h(start), 0, start)]
        prev = {start: None}
        g = {start: 0}
        order = []
        while open_heap:
            _, cost, cur = heapq.heappop(open_heap)
            if cur in order: continue
            order.append(cur)
            if cur == end: break
            for n in self._neighbors(*cur):
                ng = cost + 1
                if n not in g or ng < g[n]:
                    g[n] = ng
                    prev[n] = cur
                    heapq.heappush(open_heap, (ng + h(n), ng, n))
        if end not in prev: return None
        path, c = [], end
        while c: path.insert(0, c); c = prev[c]
        return order, path

    def _animate(self, explored, path, algo_name):
        self.solving = True
        i = [0]

        def step():
            if not self.solving: return
            if i[0] <= len(explored):
                self._draw_all(explored[:i[0]])
                i[0] += 1
                self.anim_id = self.root.after(15, step)
            else:
                self._draw_all(explored, path)
                self.status_var.set(
                    f"{algo_name}: {len(explored)} sel dieksplorasi, jalur {len(path)} langkah."
                )
                self.solving = False

        step()


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
