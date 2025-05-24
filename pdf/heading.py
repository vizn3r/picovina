import fitz


def is_green(color_int):
    r = (color_int >> 16) & 0xFF
    g = (color_int >> 8) & 0xFF
    b = color_int & 0xFF
    target = (0, 176, 80)
    dist = ((r - target[0]) ** 2 + (g - target[1]) ** 2 + (b - target[2]) ** 2) ** 0.5
    return dist < 30


def clean_text(text):
    return "".join(ch for ch in text if ch.isprintable() or ch in " \t\n\r").strip()


def starts_with_uppercase(text):
    # Check if first letter (ignoring whitespace) is uppercase (ASCII or Unicode)
    for ch in text:
        if ch.isalpha():
            return ch == ch.upper()
    return False


def extract_questions_and_green_answers(pdf_path, txt_path):
    doc = fitz.open(pdf_path)

    output_lines = []
    current_heading = None
    current_answers = []

    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] != 0:
                continue

            for line in b["lines"]:
                # Collect all text spans
                full_line_text = ""
                green_spans = []
                for span in line["spans"]:
                    cleaned = clean_text(span["text"])
                    if not cleaned:
                        continue
                    full_line_text += cleaned + " "
                    if is_green(span["color"]):
                        green_spans.append(cleaned)

                full_line_text = full_line_text.strip()
                if not full_line_text:
                    continue

                # If line starts with uppercase letter, treat as heading
                if starts_with_uppercase(full_line_text):
                    # If we had a previous question, write it out
                    if current_heading is not None and current_answers:
                        output_lines.append(current_heading)
                        output_lines.extend(["• " + ans for ans in current_answers])
                        output_lines.append("")  # blank line separator

                    current_heading = full_line_text
                    current_answers = []

                # Else if line has green spans, treat as answer line
                elif green_spans and current_heading is not None:
                    # Add all green spans as separate answers
                    current_answers.extend(green_spans)

                # Else ignore line (could be explanatory text, etc.)

    # Write last question group
    if current_heading is not None and current_answers:
        output_lines.append(current_heading)
        output_lines.extend(["• " + ans for ans in current_answers])

    with open(txt_path, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(
        f"Extracted {len(output_lines)} lines (headings + green answers) to {txt_path}"
    )


if __name__ == "__main__":
    extract_questions_and_green_answers("ans.pdf", "ans.txt")
