latex_template = r"""
\documentclass{article}
\usepackage{geometry}
\geometry{margin=1in}
\title{PDF Concept Summary}
\date{}

\begin{document}
\maketitle
\tableofcontents
\newpage

%CONTENT%

\end{document}
"""

def section_for_pdf(title, concepts, questions, raw_text):
    s = f"\\section{{{title}}}\n"

    s += "\\subsection*{Concepts}\n"
    for c in concepts:
        s += f"- {c}\n"

    s += "\n\\subsection*{Questions}\n"
    for q in questions:
        s += f"- {q}\n"

    s += "\n\\subsection*{Extracted Text}\n"
    s += "\\begin{verbatim}\n" + raw_text[:4000] + "\n\\end{verbatim}\n"

    return s

def section_for_relationships(related):
    if not related:
        return "\\section{Concept Relationships}\nNo related concepts detected.\n"

    s = "\\section{Concept Relationships}\n"
    for c1, c2, score in related:
        s += f"{c1} ↔ {c2} (Similarity: {score})\n\n"
    return s
