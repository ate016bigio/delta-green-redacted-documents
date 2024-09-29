from reportlab.lib.pagesizes import legal
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.fonts import tt2ps
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import fonts
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from PIL import Image as PILImage
from utils import wrap_text
from utils import redact_in_line

# output_path = 'example.pdf'
# page_size = (673, 930)
# margin = 2
# background_image_path = './assets/page.png'
# font_name = "times"
# font_size = 11
# lines = ['Hello '*50, 'there']


def pdf_generator(
        input_path: str,
        output_path: str,
        page_size: tuple[int, int] = (673, 930),
        margin: int = 2,
        background_image_path: str = '../assets/page.png',
        font_name: str = "times",
        font_size: int = 11,
) -> None:
    with open(input_path, 'r') as file:
        lines = file.readlines()
    pdf = canvas.Canvas(output_path, pagesize=page_size)
    width, height = page_size
    margin_in_pixels = margin * inch
    available_width = width - 2 * margin_in_pixels

    if background_image_path:
        pdf.drawImage(background_image_path, 0, 0, width=width, height=height)

    pdfmetrics.registerFont(TTFont(font_name, f'{font_name}.ttf'))
    pdf.setFont(font_name, font_size)

    y_position = height - margin_in_pixels
    for line in lines:
        wrapped_lines = wrap_text(line.strip(), font_size, available_width, pdf)
        for wrapped_line in wrapped_lines:
            if y_position < margin_in_pixels:  # If we are near the bottom, add a new page
                pdf.showPage()  # Move to a new page
                y_position = height - margin_in_pixels  # Reset y_position for the new page
                pdf.setFont(font_name, font_size)
                if background_image_path:
                    pdf.drawImage(background_image_path, 0, 0, width=width, height=height)

            redacted_line = redact_in_line(wrapped_line, font_name, font_size, margin_in_pixels, y_position + 10, pdf)
            pdf.setFillColorRGB(0, 0, 0)  # Set text color to black
            pdf.drawString(margin_in_pixels, y_position, redacted_line)
            pdf.drawString(margin_in_pixels, y_position, redacted_line)  # Draw text line by line
            y_position -= font_size + 5  # Move the position for the next line
    pdf.save()
