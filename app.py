import streamlit as st
from agent.generate_offer_letter import generate_offer_letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os
import textwrap
import re

# Setup Unicode font
FONT_DIR = "fonts"
FONT_NAME = "DejaVuSans"
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font file not found at: {FONT_PATH}")

pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))

# Function to write multi-line text to PDF
def generate_pdf(letter_text, employee_name):
    safe_name = employee_name.replace(" ", "_")
    pdf_path = f"{safe_name}_offer_letter.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    c.setFont(FONT_NAME, 11)

    x_margin = inch * 0.75
    y_margin = height - inch  # Start 1 inch from top
    line_height = 14

    wrapped_lines = []
    for line in letter_text.split('\n'):
        clean_line = ''.join(c if c.isprintable() else ' ' for c in line)
        clean_line = re.sub(r'[^\x00-\x7F]+', ' ', clean_line)  # remove non-ASCII
        if clean_line.strip() == "":
            wrapped_lines.append("")
        else:
            wrapped_lines.extend(textwrap.wrap(clean_line, width=95))

    for line in wrapped_lines:
        if y_margin < inch:
            c.showPage()
            c.setFont(FONT_NAME, 11)
            y_margin = height - inch
        c.drawString(x_margin, y_margin, line)
        y_margin -= line_height

    c.save()
    return pdf_path

# Streamlit UI
st.title("📄 Offer Letter Generator")

employee_name = st.text_input("Enter employee name:")
submit = st.button("Generate Offer Letter")

if submit and employee_name:
    with st.spinner("Generating offer letter..."):
        try:
            letter = generate_offer_letter(employee_name)
            if letter and isinstance(letter, str) and len(letter.strip()) > 20:
                st.success("Offer letter generated successfully!")
                st.text_area("Offer Letter:", letter, height=400)

                pdf_path = generate_pdf(letter, employee_name)

                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="📥 Download as PDF",
                        data=f,
                        file_name=pdf_path,
                        mime="application/pdf"
                    )
            else:
                st.error("Offer letter is empty or invalid. Check name spelling or data.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
