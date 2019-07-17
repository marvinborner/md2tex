#!/bin/env python
import re
from sys import argv

path = argv[1]
data = list(filter(None, [line.rstrip("\n") for line in open(path)]))
latex = [
    "\\documentclass[11pt]{article}",
    "\\usepackage[utf8]{inputenc}",
    "\\usepackage{hyperref}",
    "\\usepackage{ulem}",
    "\\usepackage{listings}",
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
    r"[0-9]+\. (.*)": "ol",  # Ordered list
    r"```(.*)": "code",  # Coding
    r"\|(.*)\|": "table",  # Table
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
                elif rules[rule] in ("ul", "ol"):
                    list_type = "itemize" if rules[rule] == "ul" else "enumerate"
                    if re.match(rule, data[i - 1]):
                        new_line = "\\item " + matched_group
                        if i + 1 == len(data) or not re.match(rule, data[i + 1]):
                            new_line += " \\end{" + list_type + "}"
                    else:
                        new_line = "\\begin{" + list_type + "} \\item " + matched_group
                elif rules[rule] == "code":
                    found = i
                    while True:
                        found = found + 1 if found > len(data) else i
                        if "```" in data[found]:
                            break
                    new_line = "\\begin{lstlisting}[language=" + matched_group + "]\n" + "\n".join(data[i + 1:found]) + "\\end{lstlisting}"
                elif rules[rule] == "table":
                    found = i
                    table = [matched_group.split("|")]
                    while True:
                        found = found + 1
                        if re.match(rule, data[found]):
                            table.append((re.match(rule, data[found]).groups()[0]).split("|"))
                            data[found] = ""
                        else:
                            data[i] = ""
                            break
                    new_line = "\\begin{table}[] \\begin{tabular}{" + ("c" * len(table[0])) + "} "
                    for k, row in enumerate(table):
                        for l, element in enumerate(row):
                            new_line += element
                            if l + 1 != len(row):
                                new_line += "&"
                        if k + 1 != len(table):
                            new_line += "\\\\ \n"
                    new_line += "\\end{tabular} \\end{table}"
                    # print(table)
    if line[-2:] == "  ":
        new_line += "\\\\"
    latex.append(new_line)

latex.append("\\end{document}")
open("output.tex", "w").write("\n".join(latex))
print(latex)
