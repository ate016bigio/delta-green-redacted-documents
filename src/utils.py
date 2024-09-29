import re

from reportlab.pdfgen import canvas


def wrap_text(text: str, font_size: int, available_width: float, pdf) -> list[str]:
    """Wrap text into lines that fit within the available width."""
    words = text.split()
    wrapped_lines = []
    current_line = ""

    for word in words:
        # Measure the width of the current line if we add this word
        test_line = current_line + " " + word if current_line else word
        if pdf.stringWidth(test_line, fontSize=font_size) <= available_width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line)
            current_line = word  # Start a new line with the current word

    # Add the last line
    if current_line:
        wrapped_lines.append(current_line)

    return wrapped_lines


def redact_in_line(
        line: str,
        font_name: str,
        font_size: int,
        margin_in_pixels: int,
        y_position: int,
        pdf: canvas.Canvas,
) -> str:
    """Redact content between **...** in a given line."""
    # Find all matches of content between **...**
    matches = list(re.finditer(r"\*\*(.*?)\*\*", line))

    if not matches:
        # If no redaction needed, return the original line
        return line

    # We need to handle redaction
    redacted_line = line
    total_offset = 0

    for match in matches:
        start, end = match.span()

        # Calculate the width of the text before the redaction
        visible_text = redacted_line[:start - total_offset]
        text_width_before = pdf.stringWidth(visible_text, font_name, font_size)

        # Calculate the width of the redacted content
        redacted_text_width = pdf.stringWidth("1" * (end - start - 4), font_name, font_size)

        # Draw a black rectangle over the redacted portion
        x_position = margin_in_pixels + text_width_before
        pdf.setFillColorRGB(0, 0, 0)  # Set to black for the rectangle
        pdf.rect(x_position, y_position - font_size, redacted_text_width, font_size, fill=1)

        # Replace the redacted portion with spaces
        redacted_line = (redacted_line[:start - total_offset]
                         + "1" * (end - start - 4)
                         + redacted_line[end - total_offset:])
        total_offset += (end - start)

    return redacted_line
