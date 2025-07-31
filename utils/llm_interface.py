import os
import google.generativeai as genai
from dotenv import load_dotenv
from agent.generate_offer_letter import get_all_employee_names

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def extract_name_and_validate(user_input):
    valid_names = get_all_employee_names()
    names_list = "\n".join(valid_names[:100])  # cap to first 100 for token safety

    prompt = f"""
You are an assistant that extracts and validates a candidate name.

Valid employee names (case-insensitive):
{names_list}

User request: "{user_input}"

If the user asked for an offer letter:
  • If the extracted name exactly matches one of the valid names, respond with:
    valid:<Exact Matched Name>
  • Otherwise respond with:
    invalid:<Brief explanation why no match>
Do not say anything else.
"""

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        resp = model.generate_content(prompt)
        content = resp.text.strip()

        lower = content.lower()
        if lower.startswith("valid:"):
            name = content.split("valid:", 1)[1].strip()
            return "valid", name
        if lower.startswith("invalid:"):
            reason = content.split("invalid:", 1)[1].strip()
            return "invalid", reason

        # LLM didn’t follow the format
        return "invalid", "I didn’t understand which name you meant. Please try again."

    except Exception as e:
        return "error", f"LLM error: {e}"
