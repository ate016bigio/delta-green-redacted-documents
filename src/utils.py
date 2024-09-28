
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