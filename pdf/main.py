from pdfminer.high_level import extract_pages
from pdfminer.layout import LTChar, LTTextLineHorizontal, LTTextBoxHorizontal
from pathlib import Path


def is_colored(char):
    try:
        return char.graphicstate.ncolor != (0.0, 0.0, 0.0)
    except AttributeError:
        return False


def extract_colored_lines(pdf_path):
    colored_lines = []
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                for line in element:
                    if isinstance(line, LTTextLineHorizontal):
                        if any(isinstance(c, LTChar) and is_colored(c) for c in line):
                            colored_lines.append(line.get_text().strip())
    return colored_lines


def save_lines_to_file(lines, output_path):
    with open(output_path, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\n")


if __name__ == "__main__":
    input_pdf = "ans.pdf"  # Replace with your PDF
    output_txt = "ans.txt"  # Output file

    if not Path(input_pdf).exists():
        print(f"Error: File not found: {input_pdf}")
        exit(1)

    print(f"Extracting colored lines from: {input_pdf}")
    lines = extract_colored_lines(input_pdf)

    if lines:
        save_lines_to_file(lines, output_txt)
        print(f"Saved {len(lines)} colored line(s) to: {output_txt}")
    else:
        print("No colored lines found.")
