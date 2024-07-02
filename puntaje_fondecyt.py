# ADS query: %6.6m|%T|%Y|%c
from argparse import ArgumentParser
import numpy as np

parser = ArgumentParser()
parser.add_argument("filename", default="bibliografia.txt")
args = parser.parse_args()

titles = []
pts = []
li = []
ci = []
idx_points = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.2]
i = 0
with open(args.filename) as f:
    for line in f:
        authors, title, year, citations = line.split("|")
        titles.append(title)
        authors = [a.strip() for a in authors.replace("&", ",").split(",")]
        if "Sifón" in authors:
            author_idx = authors.index("Sifón")
        else:
            author_idx = 6
        ci.append(int(citations) / max([1, 2023 - int(year)]))
        li.append(idx_points[author_idx])
        print(line, author_idx, ci[-1], li[-1])
ci = np.array(ci)
li = np.array(li)
pts = li * (1 + ci) ** 0.5
nota = 1 + 1.7 * np.cumsum(pts) ** 0.25
titles = np.array(titles)

j = np.argsort(-pts)
titles = titles[j]
pts = pts[j]
li = li[j]
ci = ci[j]
print()
print(" #  | Title | l_i | c_i | puntaje | nota final")
for i in range(pts.size):
    print(
        f"{i:2d} | {titles[i][:50]:50s} | {li[i]:.2f} | {ci[i]:6.2f} | {pts[i]:.1f} | {nota[i]:5.2f}"
    )
