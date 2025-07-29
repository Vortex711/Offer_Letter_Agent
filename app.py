import streamlit as st
from agent.generate_offer_letter import generate_offer_letter

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

                # PDF logic unchanged

                
                # Option to download as PDF
                from fpdf import FPDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                pdf.set_font("Arial", size=12)

                for line in letter.split('\n'):
                    pdf.multi_cell(0, 10, line)

                safe_name = employee_name.replace(" ", "_")
                pdf_path = f"{safe_name}_offer_letter.pdf"

                pdf.output(pdf_path)

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
