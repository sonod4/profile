import re
import pikepdf
import fitz  # PyMuPDF


def recolor_all_strokes(input_pdf: str,
                        output_pdf: str):
    """
    Change every vector stroke (RG, G) and fill (rg, g) in a PDF to the given RGB.
    """
    # Desired color triples
    grid_rgb = f"0.075 0.231 0.341 RG"  # stroking RGB (DeviceRGB) :contentReference[oaicite:0]{index=0}
    black_rgb   = f"0.929 0.922 0.914 rg"  # non-stroking RGB :contentReference[oaicite:1]{index=1}
    black_RGb   = f"0.929 0.922 0.914 RG"  # non-stroking RGB :contentReference[oaicite:1]{index=1}

    # Patterns for grayscale operators
    gray_stroke_pattern = re.compile(r"\b0(\.0+)?\s+G\b")   # '0 G' sets stroking gray :contentReference[oaicite:3]{index=3}
    # gs_pattern          = re.compile(r"/GS\d+\s+gs")        # graphic-state overrides :contentReference[oaicite:4]{index=4}
    gray_fill_pattern   = re.compile(r"\b0(\.0+)?\s+g\b")   # '0 g' sets non-stroking gray :contentReference[oaicite:2]{index=2}
    rgb_stroke_pattern  = re.compile(r"\d+(\.\d+)?\s+\d+(\.\d+)?\s+\d+(\.\d+)?\s+RG")
    rgb_fill_pattern    = re.compile(r"\d+(\.\d+)?\s+\d+(\.\d+)?\s+\d+(\.\d+)?\s+rg")

    # Open the PDF
    pdf = pikepdf.Pdf.open(input_pdf)                     # working with content streams :contentReference[oaicite:5]{index=5}

    for page in pdf.pages:
        # Normalize page.Contents to a list
        contents = page.Contents
        streams = contents if isinstance(contents, list) else [contents]  # :contentReference[oaicite:6]{index=6}

        new_streams = []
        for stream in streams:
            # Decode raw bytes preserving exact byte values
            raw = stream.read_bytes().decode('latin1')    # latin1 preserves 0–255 bytes :contentReference[oaicite:7]{index=7}
            # print(raw)
            # _ = raw
            raw = raw.replace("0 0.31 0.545 rg","0.459 0.749 1 rg") # dark blue strokes into light blue
            raw = raw.replace("1 0.6 0.8 rg","0.541 0 0.271 rg") # purple highlight of texts
            raw = raw.replace("\n0 0.549 0.227 rg","0.451 1 0.678 rg") # green text

            raw = raw.replace("0 0.31 0.545 RG","0.459 0.749 1 RG") # green text
            # raw = raw.replace("0.0745 0.231 0.341 RG","0.459 0.749 1 RG") # green text
            # print(raw)
            # 1) Strip any graphic-state that may reset color
            # raw = gs_pattern.sub("", raw) # nothing

            # 2) Replace existing RGB strokes/fills (colored shapes)
            # raw = rgb_stroke_pattern.sub(grid_rgb, raw) # grid
            # raw = rgb_fill_pattern.sub(grid_rgb, raw) # colorolored strokes

            # 3) Replace pure-black grayscale: '0 G' and '0 g'
            raw = gray_stroke_pattern.sub(black_RGb, raw) # nothing
            raw = gray_fill_pattern.sub(black_rgb, raw) # black strokes

            # 4) Create a new stream and collect
            new_streams.append(pdf.make_stream(raw.encode('latin1')))  # reattach via make_stream :contentReference[oaicite:8]{index=8}

        # Reassign modified streams back to the page
        page.Contents = new_streams if len(new_streams) > 1 else new_streams[0]

    # Save the recolored PDF
    pdf.save(output_pdf, linearize=True)                  # preserves compression & refs :contentReference[oaicite:9]{index=9}
    pdf.close()

def recolor_strokes(input_pdf, output_pdf):
    doc = fitz.open(input_pdf)

    bg_new = (0.125, 0.122, 0.118) # black

    for page in doc:
        drawings = page.get_drawings()

        # add new color background
        rect = page.rect
        page.draw_rect(rect, fill=bg_new, overlay=False)

    doc.save(output_pdf)
    print(f"Saved updated PDF to '{output_pdf}'.")




recolor_all_strokes("input_file.pdf","output_.pdf")
recolor_strokes(input_pdf = "output_.pdf",output_pdf="output_file.pdf")
