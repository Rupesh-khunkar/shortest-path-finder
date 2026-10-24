"""Builds the project report PDF.

Usage:
    pip install reportlab
    python report/build_report.py --url https://github.com/<user>/<repo>.git --name "Your Name"
"""
import argparse
import json
import os
import sys

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph,
                                SimpleDocTemplate, Spacer, Table, TableStyle)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

NAVY = colors.HexColor("#1F3A5F")
LIGHT = colors.HexColor("#E6EFF5")
LINE = colors.HexColor("#B8C7D3")

ap = argparse.ArgumentParser()
ap.add_argument("--url", default="https://github.com/YOUR-USERNAME/shortest-path-finder-daa.git")
ap.add_argument("--name", default="")
ap.add_argument("--out", default=os.path.join(ROOT, "Shortest_Path_Finder_DAA_Report.pdf"))
args = ap.parse_args()

ss = getSampleStyleSheet()
body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.5, leading=13.5)
small = ParagraphStyle("small", parent=body, fontSize=8, textColor=colors.HexColor("#555555"))
cap = ParagraphStyle("cap", parent=small, alignment=TA_CENTER)
cell = ParagraphStyle("cell", parent=body, fontSize=9, leading=12)
cellb = ParagraphStyle("cellb", parent=cell, fontName="Helvetica-Bold")
th = ParagraphStyle("th", parent=cellb, textColor=colors.white)
title = ParagraphStyle("title", parent=ss["Title"], fontName="Helvetica-Bold", fontSize=26, leading=34)
sub = ParagraphStyle("sub", parent=body, alignment=TA_CENTER, textColor=colors.HexColor("#555555"), fontSize=11)
h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=15, textColor=NAVY,
                    spaceBefore=10, spaceAfter=4, keepWithNext=1)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=12, bulletIndent=2, spaceAfter=3)


def P(t, s=body): return Paragraph(t, s)
def B(t): return Paragraph(t, bullet, bulletText="\u2022")


def kv_table(rows, w1=45 * mm, w2=125 * mm):
    t = Table([[P(k, cellb), P(v, cell)] for k, v in rows], colWidths=[w1, w2])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (0, -1), LIGHT), ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def grid_table(header, rows, widths, dark=True, align_right=()):
    data = [[P(h, th if dark else cellb) for h in header]] + [[P(str(c), cell) for c in r] for r in rows]
    t = Table(data, colWidths=widths, repeatRows=1)
    st = [("GRID", (0, 0), (-1, -1), 0.4, LINE), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("BACKGROUND", (0, 0), (-1, 0), NAVY if dark else LIGHT),
          ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]
    t.setStyle(TableStyle(st))
    return t


def img(path, width):
    from PIL import Image as PI
    w, h = PI.open(path).size
    return Image(path, width=width, height=width * h / w)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 15 * mm, A4[0] - 20 * mm, 15 * mm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawString(20 * mm, 10.5 * mm, "Shortest Path Finder Demonstration \u2014 DAA Mini Project")
    canvas.drawRightString(A4[0] - 20 * mm, 10.5 * mm, f"Page {doc.page}")
    canvas.restoreState()


S = []
# ---------------- Page 1 ----------------
S += [Spacer(1, 14 * mm), P("SHORTEST PATH FINDER<br/>DEMONSTRATION", title),
      P("DAA Mini Project \u2022 Programming Language: Python 3", sub)]
if args.name:
    S += [Spacer(1, 2 * mm), P(f"Submitted by: <b>{args.name}</b>", sub)]
S += [Spacer(1, 8 * mm), kv_table([
    ("Project Type", "Design and Analysis of Algorithms Mini Project"),
    ("Problem Domain", "Graph algorithms / route planning"),
    ("Programming Language", "Python 3.10+"),
    ("Algorithms Demonstrated", "Dijkstra, Bellman\u2013Ford, Floyd\u2013Warshall"),
    ("Repository", "GitHub repository containing source code, README, tests, screenshots and this report")]),
    P("Submission Contents", h1),
    B("<b>GitHub Repository Link:</b> The repository URL submitted with the project."),
    B("<b>Source Code:</b> Python implementation with separate algorithm, utility and test modules."),
    B("<b>Project Report:</b> This PDF containing the problem, objectives, algorithm design, flowchart, technologies, "
      "complexity analysis, test cases, output screenshots and conclusion."),
    P("Project Overview", h1),
    P("The Shortest Path Problem is modeled as a weighted directed graph in which locations are vertices and travel "
      "costs (distance or time) are edge weights. The project demonstrates three solution strategies: a greedy "
      "single-source algorithm, a dynamic-programming single-source algorithm that supports negative weights, and a "
      "dynamic-programming all-pairs algorithm. Their capabilities and computational behavior are compared to "
      "illustrate important DAA trade-offs."), Spacer(1, 3 * mm),
    kv_table([("Single-source methods", "Dijkstra (greedy) and Bellman\u2013Ford (dynamic programming)"),
              ("All-pairs method", "Floyd\u2013Warshall (dynamic programming)"),
              ("Validation", "Automated unit tests and matrix validation"),
              ("Benchmarking", "Runtime measurement using time.perf_counter()")]),
    PageBreak()]

# ---------------- Page 2 ----------------
S += [P("1. Introduction", h1),
      P("The shortest path problem is a classic graph optimization problem and an important example for studying "
        "algorithm design. Given a network of locations and the cost of travelling along each road, the objective is "
        "to find the minimum-cost route from a source to a destination (or between all pairs of locations). It is "
        "used in GPS navigation, network routing and logistics. This project uses it to demonstrate how different "
        "algorithmic techniques affect capability, running time and scalability."),
      P("2. Problem Statement", h1),
      P("Given a weighted directed graph G = (V, E) with edge weights w(u, v) and a source vertex s, find the "
        "minimum-cost path from s to every other vertex (single-source), and optionally between every pair of "
        "vertices (all-pairs). The project must also detect unreachable vertices and negative-weight cycles, and "
        "compare the efficiency of the algorithms."),
      P("3. Objectives", h1),
      B("Model the road network as a weighted graph using an adjacency matrix."),
      B("Implement a greedy algorithm and two Dynamic Programming algorithms."),
      B("Establish correctness of the implemented approaches."),
      B("Analyze time and space complexity."),
      B("Measure practical execution time and compare algorithm behavior."),
      P("4. Algorithm Design", h1),
      kv_table([
          ("Dijkstra", "Keep a min-heap of (distance, vertex). Repeatedly extract the closest unfinalized vertex and "
                       "relax its outgoing edges. Greedy choice: the closest vertex's distance is final. "
                       "Requires non-negative weights."),
          ("Bellman\u2013Ford", "Initialize dist[s] = 0. Relax every edge V\u22121 times; if an edge can still be "
                                "relaxed in the V-th pass, a negative cycle exists. Handles negative weights."),
          ("Floyd\u2013Warshall", "Define dist[i][j] after considering intermediate vertices 0..k. Update "
                                  "dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j]) for every k. Gives "
                                  "all-pairs shortest paths.")], 35 * mm, 135 * mm),
      P("5. Correctness", h1),
      P("Dijkstra is correct because, with non-negative weights, the vertex with the smallest tentative distance "
        "cannot be improved by any later path (greedy-choice property). Bellman\u2013Ford is correct because after i "
        "passes all shortest paths using at most i edges are found, and a shortest simple path has at most V\u22121 "
        "edges. Floyd\u2013Warshall is correct by optimal substructure: the best path through intermediate vertices "
        "{0..k} either avoids k or passes through k exactly once. All three were cross-checked against each other "
        "on random graphs by the automated tests."),
      PageBreak()]

# ---------------- Page 3 ----------------
S += [P("6. Flowchart", h1),
      Table([[img(os.path.join(ROOT, "screenshots/flowchart.png"), 112 * mm)]], colWidths=[170 * mm]),
      P("Figure 1. Overall shortest-path processing flow", cap),
      P("7. Technologies / Programming Language", h1),
      P("Python 3.10+ and standard-library modules are used (heapq for the priority queue). Automated tests use "
        "unittest and runtime measurement uses time.perf_counter(). No external runtime dependencies are required."),
      P("8. Complexity Analysis (Time &amp; Space)", h1),
      grid_table(["Algorithm", "Time", "Space", "Negative edges?", "Type"], [
          ["Dijkstra (binary heap)", "O((V + E) log V)", "O(V)", "No", "Single-source"],
          ["Bellman\u2013Ford", "O(V \u00d7 E)", "O(V)", "Yes (detects cycles)", "Single-source"],
          ["Floyd\u2013Warshall", "O(V<super>3</super>)", "O(V<super>2</super>)", "Yes (detects cycles)", "All-pairs"]],
                 [38 * mm, 36 * mm, 24 * mm, 40 * mm, 32 * mm]), Spacer(1, 3 * mm),
      P("Dijkstra is the fastest because its greedy choice avoids re-scanning edges, but it cannot handle negative "
        "weights. Bellman\u2013Ford pays an extra factor of V to support negative weights and cycle detection. "
        "Floyd\u2013Warshall solves every source at once in cubic time, which is efficient only for dense or small "
        "graphs."),
      PageBreak()]

# ---------------- Page 4 ----------------
S += [P("9. Test Cases and Output Screenshots", h1),
      grid_table(["Test", "Condition", "Expected Result"], [
          ["TC01", "5-node sample graph from A", "Distances 0, 10, 50, 30, 60 from all algorithms"],
          ["TC02", "Graph with a negative edge", "Bellman\u2013Ford / Floyd correct; Dijkstra rejects input"],
          ["TC03", "Graph with a negative cycle", "NegativeCycleError raised"],
          ["TC04", "Single node and unreachable node", "Distance 0; unreachable = INF, empty path"],
          ["TC05", "Random graphs (5, 10, 25 nodes)", "All three algorithms agree for every source"],
          ["TC06", "Path reconstruction", "Path A \u2192 D \u2192 C \u2192 E"],
          ["TC07", "Invalid matrix", "Validation error"]],
                 [20 * mm, 65 * mm, 85 * mm], dark=False), Spacer(1, 3 * mm),
      P("<b>Sample input:</b> 5-node distance matrix (INF = no direct road)"), Spacer(1, 1.5 * mm),
      grid_table(["", "A", "B", "C", "D", "E"], [
          ["A", 0, 10, "INF", 30, 100], ["B", "INF", 0, 50, "INF", "INF"], ["C", "INF", "INF", 0, "INF", 10],
          ["D", "INF", "INF", 20, 0, 60], ["E", "INF", "INF", "INF", "INF", 0]],
                 [14 * mm] + [18 * mm] * 5, dark=False),
      P("The shortest distance from A to E is 60 (path A \u2192 D \u2192 C \u2192 E); the direct edge A \u2192 E "
        "costs 100."), Spacer(1, 3 * mm),
      Table([[img(os.path.join(ROOT, "screenshots/fig2_main_menu.png"), 80 * mm),
              img(os.path.join(ROOT, "screenshots/fig3_algorithm_result.png"), 80 * mm)],
             [P("Figure 2. Main menu", cap), P("Figure 3. Algorithm result", cap)]],
            colWidths=[85 * mm, 85 * mm], style=[("VALIGN", (0, 0), (-1, 0), "TOP")]),
      Spacer(1, 3 * mm),
      PageBreak()]

# ---------------- Page 5 ----------------
rows = json.load(open(os.path.join(ROOT, 'screenshots', 'bench.json')))
S += [img(os.path.join(ROOT, "screenshots/fig5_unit_tests.png"), 62 * mm),
      P("Figure 4. All 7 automated unit tests pass", cap),
      P("10. Performance Comparison", h1),
      grid_table(["Nodes", "Algorithm", "Sum of distances", "Median Time (sec)"],
                 [[n, a, c, f"{t:.8f}"] for n, a, c, t in rows], [25 * mm, 55 * mm, 45 * mm, 45 * mm]),
      Spacer(1, 3 * mm),
      img(os.path.join(ROOT, "screenshots/fig4_performance.png"), 68 * mm),
      P("Figure 5. Performance comparison generated by the project", cap),
      P("Measured runtime depends on hardware and runtime conditions; asymptotic complexity is the primary "
        "theoretical comparison. All three algorithms return identical distances (same sum), while Floyd\u2013Warshall "
        "grows fastest because it computes all pairs.", small),
      P("11. Conclusion", h1),
      P("The project connects graph modeling, greedy design, Dynamic Programming, correctness, complexity analysis, "
        "testing and practical benchmarking. The three methods make the trade-off between speed and capability "
        "visible: Dijkstra is fastest but needs non-negative weights, Bellman\u2013Ford supports negative weights, "
        "and Floyd\u2013Warshall answers every pair at higher cost."),
      P("12. Future Scope", h1),
      P("A* search, bidirectional Dijkstra, Johnson's algorithm, graphical visualization, benchmark plots and real "
        "map data can be added."),
      P("13. Repository / Execution", h1),
      P(f'<link href="{args.url}" color="blue"><u>{args.url}</u></link>')]

doc = SimpleDocTemplate(args.out, pagesize=A4, leftMargin=20 * mm, rightMargin=20 * mm, topMargin=16 * mm,
                        bottomMargin=20 * mm, title="Shortest Path Finder Demonstration \u2014 DAA Mini Project")
doc.build(S, onFirstPage=footer, onLaterPages=footer)
print("Report written to", args.out)
