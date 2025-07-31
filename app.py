import streamlit as st
from agent.generate_offer_letter import generate_offer_letter, get_all_employee_names
from utils.llm_interface import extract_name_and_validate
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import inch
import os
import textwrap
import re

# --- Setup fonts ---
FONT_DIR = "fonts"
FONT_NAME = "DejaVuSans"
BOLD_FONT_NAME = "DejaVuSans-Bold"
FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans.ttf")
BOLD_FONT_PATH = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Font file not found at: {FONT_PATH}")
if not os.path.exists(BOLD_FONT_PATH):
    raise FileNotFoundError(f"Bold font file not found at: {BOLD_FONT_PATH}")

pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH))
pdfmetrics.registerFont(TTFont(BOLD_FONT_NAME, BOLD_FONT_PATH))

# --- PDF Generation Function ---
def generate_pdf(letter_text, employee_name):
    if not employee_name:
        raise ValueError("Cannot generate PDF: employee_name is None")

    safe_name = employee_name.replace(" ", "_")
    pdf_path = f"{safe_name}_offer_letter.pdf"
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    x_margin = inch * 0.75
    y_margin = height - inch
    line_height = 14
    font_size = 11

    for line in letter_text.split('\n'):
        if y_margin < inch:
            c.showPage()
            y_margin = height - inch

        parts = re.split(r'(\*\*.*?\*\*)', line)
        x_cursor = x_margin

        for part in parts:
            if part.startswith("**") and part.endswith("**"):
                text = part[2:-2]
                c.setFont(BOLD_FONT_NAME, font_size)
            else:
                text = part
                c.setFont(FONT_NAME, font_size)

            text = ''.join(c_ if c_.isprintable() else ' ' for c_ in text)
            text = re.sub(r'[^\x00-\x7F]+', ' ', text)

            wrapped = textwrap.wrap(text, width=95)
            for subline in wrapped:
                c.drawString(x_cursor, y_margin, subline)
                y_margin -= line_height
                x_cursor = x_margin

        if not parts:
            y_margin -= line_height

    c.save()
    return pdf_path

# --- Streamlit Chat UI ---
st.title("💬 Offer Letter Chat Agent")

if "messages" not in st.session_state:
    st.session_state.messages = []

user_input = st.chat_input("Ask me to generate an offer letter...")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            status, value = extract_name_and_validate(user_input)

            if status == "valid" and value:
                try:
                    letter = generate_offer_letter(value)
                    st.markdown("✅ Here's the generated offer letter:")
                    st.text_area("Offer Letter", letter, height=400)

                    pdf_path = generate_pdf(letter, value)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            label="📥 Download PDF",
                            data=f,
                            file_name=pdf_path,
                            mime="application/pdf"
                        )

                    st.session_state.messages.append(
                        {"role": "assistant", "content": f"✅ Offer letter for **{value}** generated successfully."}
                    )
                except Exception as e:
                    err_msg = f"⚠️ Something went wrong while generating the PDF. {str(e)}"
                    st.markdown(err_msg)
                    st.session_state.messages.append({"role": "assistant", "content": err_msg})

            elif status == "invalid":
                # value is the human-friendly reason from the LLM
                explanation = value or "Sorry, I couldn't find that employee. Please check the name and try again."
                st.markdown(f"❌ {explanation}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"❌ Hmm, I couldn't generate the offer letter. {explanation}"
                })

            elif status == "error":
                # value is the error message (e.g. API issues)
                error_msg = value or "Something went wrong on my side. Please try again shortly."
                st.markdown(f"⚠️ {error_msg}")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": f"⚠️ Oops! There was an error: {error_msg}"
                })

            else:
                # Should never hit this, but just in case
                st.markdown("⚠️ Unexpected response. Please try again.")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "⚠️ Unexpected response. Let’s try again!"
                })
