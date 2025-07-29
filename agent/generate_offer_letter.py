from embeddings.query_vector_store import query_vector_store
from parsing.parse_csv import load_employee_data
import os
import google.generativeai as genai

# Load Gemini
genai.configure(api_key="AIzaSyAr_ZOxZAufdQv9hgtwNBfxjVlahXHUVas")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load CSV once
EMPLOYEE_CSV_PATH = "data/Employee_List.csv"
employee_df = load_employee_data(EMPLOYEE_CSV_PATH)

def get_employee_metadata(name):
    print("Available columns:", employee_df.columns.tolist())  # optional debug line
    matches = employee_df[employee_df['Employee Name'].str.lower() == name.lower()]
    if matches.empty:
        return None
    return matches.iloc[0].to_dict()


def generate_offer_letter(name):
    employee = get_employee_metadata(name)
    if not employee:
        print(f"❌ No employee found with name: {name}")
        return

    # Query documents
    context_chunks = query_vector_store(f"Offer letter for {name}", top_k=5, return_docs=True)

    # Construct prompt
    context_text = "\n\n".join(context_chunks)
    prompt = f"""
You are an HR agent. Use the following information to generate a formal offer letter.

Employee Metadata:
{employee}

Relevant Policy & Sample Offer Info:
{context_text}

Write a professional offer letter addressed to the employee. Include important policies, salary info, and joining date.
"""

    print("\n📨 Generating offer letter...\n")
    response = model.generate_content(prompt)
    print(response.text)
