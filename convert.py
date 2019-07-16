#!/bin/env python
import re
from sys import argv

path = argv[1]
data = [line.rstrip("\n") for line in open(path)]
latex = [
    "\\documentclass[11pt]{article}",
    "\\usepackage[utf8]{inputenc}",
    "\\begin{document}"
]
rules = {
    "(# )(.*)": "\\section{input}",  # Caption 1
    "(## )(.*)": "\\subsection{input}",  # Caption 2
    "(### )(.*)": "\\subsubsection{input}",  # Caption 3
}

for i, line in enumerate(data):
    print(line)
    matched = False
    new_line = line
    for rule in rules:
        match = re.match(rule, new_line)
        if match:
            print(match.groups())
            matched = True
            new_line = rules[rule].replace("input", match.groups()[1])
    if new_line[-2:] == "  ":
        new_line = new_line[:-2]
        new_line += "\\\\"
    latex.append(new_line)

latex.append("\\end{document}")
open("output.tex", "w").write("\n".join(latex))
print(latex)
