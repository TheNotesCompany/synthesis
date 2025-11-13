import cv2
import pytesseract
from pytesseract import Output
import layoutparser as lp
from pdf2image import convert_from_path
import os

# -------- SETTINGS --------
INPUT_FILE = "document.pdf"   # or "page.png"
OUTPUT_DIR = "extracted_diagrams"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------- 1. CONVERT PDF TO IMAGES (if needed) --------
pages = []
if INPUT_FILE.lower().endswith(".pdf"):
    pages = convert_from_path(INPUT_FILE, dpi=300)
else:
    pages = [INPUT_FILE]

# -------- 2. LOAD LAYOUTPARSER MODEL (for diagrams) --------
model = lp.Detectron2LayoutModel(
    config_path="lp://PubLayNet/faster_rcnn_R_50_FPN_3x/config",
    label_map={0: "text", 1: "title", 2: "list", 3: "table", 4: "figure"},
    extra_config=["MODEL.ROI_HEADS.SCORE_THRESH_TEST", 0.5]
)

def extract_figures(img, page_idx):
    print(f"Processing page {page_idx+1}...")

    # Convert PIL > OpenCV if needed
    if not isinstance(img, str):
        img_cv = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    else:
        img_cv = cv2.imread(img)

    # -------- 3. RUN LAYOUT DETECTION --------
    layout = model.detect(img_cv)

    # -------- 4. FIND FIGURES (DIAGRAMS) --------
    figure_blocks = [b for b in layout if b.type == "figure"]

    if not figure_blocks:
        print("No diagrams detected on this page.")
        return

    # -------- 5. CROP AND SAVE FIGURES --------
    for i, block in enumerate(figure_blocks):
        x1, y1, x2, y2 = map(int, block.coordinates)
        crop = img_cv[y1:y2, x1:x2]

        out_path = f"{OUTPUT_DIR}/page{page_idx+1}_diagram{i+1}.png"
        cv2.imwrite(out_path, crop)
        print("Saved:", out_path)

# -------- RUN ON ALL PAGES --------
import numpy as np

for idx, page in enumerate(pages):
    extract_figures(page, idx)

print("\nDone! Extracted diagrams are inside:", OUTPUT_DIR)
