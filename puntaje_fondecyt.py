# ADS query: %6.6m|%T|%Y|%c
from argparse import ArgumentParser
from datetime import date
import numpy as np
from termcolor import colored

parser = ArgumentParser()
parser.add_argument("filename", default="bibliografia.txt")
parser.add_argument("-a", "--author", default="Sifón")
parser.add_argument("-y", "--year", default=date.today().year, type=int)
args = parser.parse_args()

titles = []
citations = []
year = []
year_factor = []
authindex = []
pts = []
li = []
ci = []
idx_points = [1, 1, 0.9, 0.7, 0.5, 0.3, 0.2]
i = 0
with open(args.filename) as f:
    for line in f:
        try:
            authors, title, yr, cit = line.split("|")
        except ValueError as e:
            print(f"Error parsing line: {line}")
            raise ValueError(e)
        titles.append(title)
        authors = authors.replace("&", ",").replace("et al.", "")
        authors = [a.strip() for a in authors.split(",")]
        if args.author in authors:
            author_idx = authors.index(args.author)
        else:
            author_idx = 6
        print(authors, author_idx)
        authindex.append(max(1, author_idx))
        citations.append(int(cit))
        year.append(int(yr))
        year_factor.append(1 / max([1, args.year - int(yr)]))
        ci.append(year_factor[-1] * int(cit))
        li.append(idx_points[author_idx])
ci = np.array(ci)
li = np.array(li)
pts = li * (1 + ci) ** 0.5
titles = np.array(titles)

j = np.argsort(-pts)
titles = titles[j]
year = np.array(year)[j]
citations = np.array(citations)[j]
year_factor = np.array(year_factor)[j]
authindex = np.array(authindex)[j]
pts = pts[j]
li = li[j]
ci = ci[j]
nota = 1 + 1.7 * np.cumsum(pts) ** 0.25
print()
print(
    colored("#", "cyan", attrs=("bold",)),
    "Título | año | factor año | autor |",
    colored("l_i", "cyan", attrs=("bold",)),
    "| citas |",
    colored("c_i", "cyan", attrs=("bold",)),
    "| puntaje | ",
    colored("nota final", "magenta", attrs=("bold",)),
    "|",
)
for i in range(pts.size):
    print(
        colored(f"{i+1:2d}", "cyan", attrs=("bold",)),
        f"| {titles[i][:80]:80s} | {year[i]} | {year_factor[i]:.2f} | {authindex[i]} |",
        colored(f"{li[i]:.2f}", "cyan", attrs=("bold",)),
        f"| {citations[i]:3d} |",
        colored(f"{ci[i]:6.2f}", "cyan", attrs=("bold",)),
        f"| {pts[i]:.2f} |",
        colored(f"{nota[i]:5.2f}", "magenta", attrs=("bold",)),
        "|",
    )
    if i + 1 == 10:
        print(136 * "-")
