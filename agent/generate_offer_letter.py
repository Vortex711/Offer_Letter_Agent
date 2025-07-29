from embeddings.query_vector_store import query_vector_store
from parsing.parse_csv import load_employee_data
import os
import google.generativeai as genai
import pandas as pd

# Load Gemini
genai.configure(api_key="AIzaSyAr_ZOxZAufdQv9hgtwNBfxjVlahXHUVas")
model = genai.GenerativeModel("gemini-1.5-flash")

# Load CSV once
EMPLOYEE_CSV_PATH = "data/Employee_List.csv"
employee_df = load_employee_data(EMPLOYEE_CSV_PATH)

def get_employee_metadata(name):
    try:
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "Employee_List.csv")
        df = pd.read_csv(csv_path)
        print("✅ Loaded employee CSV. Columns:", df.columns.tolist())
        matches = df[df['Employee Name'].str.lower().str.strip() == name.lower().strip()]


        if not matches.empty:
            return matches.iloc[0].to_dict()
        else:
            print("❌ Employee not found in CSV.")
            return None
    except Exception as e:
        print("🚨 Error loading CSV:", e)
        return None


def generate_offer_letter(name):
    print(f"🔎 Looking for: {name}")

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

    response = model.generate_content(prompt)
    print(response.text)
    return response.text

