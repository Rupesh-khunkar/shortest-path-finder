"""Generates the report figures (terminal screenshots + flowchart) from real program output.

Usage: python report/make_screenshots.py     (needs: pip install pillow matplotlib)
"""
import builtins
import contextlib
import io
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.chdir(ROOT)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from PIL import Image, ImageDraw, ImageFont  # noqa: E402

import main as app  # noqa: E402
from utils import benchmark, format_benchmark  # noqa: E402

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"
OUT = os.path.join(ROOT, "screenshots")
os.makedirs(OUT, exist_ok=True)


def term(text, name, title, size=17):
    f = ImageFont.truetype(FONT, size)
    lines = text.split("\n")
    lh = size + 6
    w = max(max(int(f.getlength(l)) for l in lines), int(f.getlength(title)) + 90) + 48
    h = lh * len(lines) + 80
    img = Image.new("RGB", (w, h), (30, 32, 38))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 34], fill=(52, 55, 64))
    for i, c in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        d.ellipse([14 + i * 22, 11, 26 + i * 22, 23], fill=c)
    d.text((100, 8), title, font=f, fill=(200, 200, 205))
    y = 50
    for l in lines:
        col = (230, 230, 235)
        if l.startswith("=") or "FINDER" in l or "COMPARISON" in l:
            col = (120, 200, 255)
        if "Enter choice" in l or l.startswith(("Source", "Target")):
            col = (160, 240, 160)
        d.text((24, y), l, font=f, fill=col)
        y += lh
    img.save(os.path.join(OUT, name))


def run(inputs):
    it = iter(inputs)

    def fake(prompt=""):
        v = next(it)
        print(prompt + v)
        return v
    builtins.input = fake
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            app.main()
        except StopIteration:
            pass
    return buf.getvalue()


BAR = "=" * 60
HEAD = f"{BAR}\n      SHORTEST PATH FINDER DEMONSTRATION\n{BAR}\n"
menu = run(["5", "0", "7"]).split("\nEnter choice: 5")[0].strip("\n") + "\n\nEnter choice: 5"
term(menu, "fig2_main_menu.png", "python main.py")

res = run(["2", "0", "5", "0", "7"]).split(HEAD)
body = lambda b: b.split("7. Exit\n")[-1].strip("\n")  # noqa: E731
term(body(res[1]) + "\n\n" + body(res[2]), "fig3_algorithm_result.png", "python main.py")

rows = benchmark(sizes=(10, 20, 40, 80), repeats=5)
json.dump(rows, open(os.path.join(OUT, "bench.json"), "w"))
term(format_benchmark(rows), "fig4_performance.png", "python main.py  [option 6]")

tests = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
                       capture_output=True, text=True).stderr
lines = []
for l in tests.strip().split("\n"):
    lines.append(l.split(" (")[0] + " ... ok" if " ... " in l else l)
term("\n".join(lines), "fig5_unit_tests.png", "python -m unittest discover -s tests -v")

# ---- flowchart ----
fig, ax = plt.subplots(figsize=(7.2, 7.4))
ax.set_xlim(0, 10); ax.set_ylim(0, 11); ax.axis("off")


def box(x, y, w, h, t, fs=8):
    ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, fill=False, lw=1.2))
    ax.text(x, y, t, ha="center", va="center", fontsize=fs)


def arrow(x1, y1, x2, y2):
    ax.annotate("", (x2, y2), (x1, y1), arrowprops=dict(arrowstyle="->", lw=1))


box(5, 10.3, 2.6, 0.7, "Start")
box(5, 8.9, 5.6, 0.8, "Read graph (adjacency matrix) and source node")
box(5, 7.5, 5.6, 0.8, "Validate matrix (square, numeric entries)")
box(5, 6.1, 5.6, 0.8, "Select shortest-path algorithm")
arrow(5, 9.95, 5, 9.3); arrow(5, 8.5, 5, 7.9); arrow(5, 7.1, 5, 6.5)
for x, t in [(1.9, "Dijkstra\nGreedy min-heap"), (5, "Bellman-Ford\nRelax edges V-1 times"),
             (8.1, "Floyd-Warshall\nDP over intermediate k")]:
    box(x, 4.1, 2.8, 1.0, t); arrow(5, 5.7, x, 4.6); arrow(x, 3.6, 5, 2.9)
box(5, 2.5, 5.6, 0.8, "Display distances, path and execution time")
box(5, 1.1, 2.6, 0.7, "End"); arrow(5, 2.1, 5, 1.45)
plt.savefig(os.path.join(OUT, "flowchart.png"), dpi=170, bbox_inches="tight")
print("Screenshots written to", OUT)
