from pathlib import Path
from scripts.extract import extract_text_from_pdf
from scripts.process import extract_concepts, extract_questions
from scripts.relate import find_related_concepts
from scripts.generate_latex import latex_template, section_for_pdf, section_for_relationships

pdf_folder = Path("./textualpdf")
output_folder = Path("./output")
(output_folder / "extracted_text").mkdir(parents=True, exist_ok=True)

all_concepts = []
all_sections = []

for pdf_file in pdf_folder.glob("*.pdf"):
    print(f"Processing: {pdf_file.name}")

    text = extract_text_from_pdf(pdf_file)

    # save raw extracted text
    (output_folder / "extracted_text" / f"{pdf_file.stem}.txt").write_text(
        text, encoding="utf-8"
    )

    concepts = extract_concepts(text)
    questions = extract_questions(text)

    all_concepts.extend(concepts)

    section = section_for_pdf(pdf_file.stem, concepts, questions, text)
    all_sections.append(section)

# AI-based concept relationship detection
related = find_related_concepts(list(set(all_concepts)))

# Add relationships section
all_sections.append(section_for_relationships(related))

# Final LaTeX output
final_tex = latex_template.replace("%CONTENT%", "\n".join(all_sections))
(output_folder / "summary.tex").write_text(final_tex, encoding="utf-8")

print("✓ Done! LaTeX saved to output/summary.tex")
