#!/bin/env python
import re
from sys import argv

path = argv[1]
data = [line.rstrip("\n") for line in open(path)]
latex = [
    "\\documentclass[11pt]{article}",
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage{hyperref}",
    "\\usepackage{ulem}",
    "\\begin{document}"
]
rules = {
    r"# (.*)": "\\section{0}",  # Caption 1
    r"## (.*)": "\\subsection{0}",  # Caption 2
    r"### (.*)": "\\subsubsection{0}",  # Caption 3
    r"\[([^\[]+)\]\(([^\)]+)\)": "\\href{1}{0}",  # URLs
    r"(\*\*|__)(.*?)\1": "\\textbf{1}",  # Bold
    r"(\*|_)(.*?)\1": "\\emph{1}",  # Emphasize/italics
    r"\~\~(.*?)\~\~": "\\sout{0}",  # Strikethrough
    r"\* (.*)": "ul",  # Unordered list
}

for i, line in enumerate(data):
    matched = False
    new_line = line
    for rule in rules:
        match = re.match(rule, new_line)
        if match:
            matched = True
            new_line = rules[rule]
            for j, matched_group in enumerate(match.groups()):
                if rules[rule][:1] == "\\":
                    new_line = new_line.replace(str(j), matched_group)
                elif rules[rule] == "ul":
                    if re.match(rule, data[i - 1]):
                        new_line = "\\item " + matched_group
                        if not re.match(rule, data[i + 1]):
                            new_line += " \\end{itemize}"
                    else:
                        new_line = "\\begin{itemize} \\item " + matched_group
    if line[-2:] == "  ":
        new_line += "\\\\"
    latex.append(new_line)

latex.append("\\end{document}")
open("output.tex", "w").write("\n".join(latex))
print(latex)
