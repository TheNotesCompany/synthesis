import cv2
import pytesseract
from pytesseract import Output
import layoutparser as lp
from pdf2image import convert_from_path
import numpy as np
import os

# -------- SETTINGS --------
INPUT_FILE = "document.pdf"   # or "page.png"
OUTPUT_DIR = "extracted_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------- 1. CONVERT PDF TO IMAGES (if needed) --------
if INPUT_FILE.lower().endswith(".pdf"):
    pages = convert_from_path(INPUT_FILE, dpi=300)
else:
    pages = [cv2.imread(INPUT_FILE)]

# -------- 2. LOAD LAYOUTPARSER MODEL (for diagrams) --------
model = lp.EfficientDetLayoutModel(
    "lp://efficientdet/PubLayNet",  # ✅ FIXED (no /model)
    label_map={0: "text", 1: "title", 2: "list", 3: "table", 4: "figure"},
)

def extract_figures(img, page_idx):
    print(f"Processing page {page_idx+1}...")

    # Convert PIL → CV2
    if not isinstance(img, np.ndarray):
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    else:
        img_cv = img

    # -------- 3. RUN LAYOUT DETECTION --------
    layout = model.detect(img_cv)

    # -------- 4. FIND FIGURES (DIAGRAMS) --------
    figure_blocks = [b for b in layout if b.type == "figure"]

    if not figure_blocks:
        print("No diagrams detected on this page.")
        return

    # -------- 5. CROP & SAVE DIAGRAMS --------
    for i, block in enumerate(figure_blocks):
        x1, y1, x2, y2 = map(int, block.coordinates)
        crop = img_cv[y1:y2, x1:x2]

        out_path = f"{OUTPUT_DIR}/page{page_idx+1}_diagram{i+1}.png"
        cv2.imwrite(out_path, crop)
        print("Saved:", out_path)


# -------- PROCESS ALL PAGES --------
for idx, page in enumerate(pages):
    extract_figures(page, idx)

print("\nDone! Extracted diagrams are inside:", OUTPUT_DIR)
