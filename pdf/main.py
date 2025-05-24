# #00b050
import fitz  # PyMuPDF
import string


def is_green(color_int):
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    target = (0, 176, 80)
    dist = ((r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2) ** 0.5
    return dist < 30


def clean_text(text):
    allowed = (
        string.ascii_letters
        + string.digits
        + string.punctuation
        + " \t\n\ráäčďéíľĺňóôŕšťúýžÁÄČĎÉÍĽĹŇÓÔŔŠŤÚÝŽ"
    )  # add accented chars if you want
    # Or simply allow all printable unicode characters, skipping control chars and weird symbols:
    # A more general approach:
    return "".join(
        ch for ch in text if ch.isprintable() and not ch.isspace() or ch == " "
    )
    # You can customize this, but .isprintable() filters out control chars like ''


def extract_green_text(pdf_path, txt_path):
    doc = fitz.open(pdf_path)
    green_lines = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] != 0:
                continue
            for line in b["lines"]:
                green_text_spans = []
                for span in line["spans"]:
                    if is_green(span["color"]):
                        cleaned = clean_text(span["text"]).strip()
                        if cleaned:
                            green_text_spans.append(cleaned)
                if green_text_spans:
                    line_text = " ".join(green_text_spans).strip()
                    if line_text:
                        green_lines.append(line_text)

    with open(txt_path, "w", encoding="utf-8") as f:
        for line in green_lines:
            f.write(line + "\n")

    print(f"Extracted {len(green_lines)} green lines to {txt_path}")


if __name__ == "__main__":
    extract_green_text("ans.pdf", "ans.txt")
