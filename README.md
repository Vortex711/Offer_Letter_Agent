# Offer Letter Generation Agent 🤖📄

This is a chat-based app that generates downloadable offer letters using natural language input and LLMs (Gemini).

## 🔧 Features

- Chat UI for natural language queries like:  
  `"Generate an offer letter for Priya Sharma"`  
- Employee name validation using an Excel/CSV metadata file  
- Generates offer letters using Google Gemini  
- Exports the letter as a downloadable PDF with bold formatting  

## 🧑‍💻 How to Run Locally

1. **Clone this repo**:
   ```bash
   git clone https://github.com/Vortex711/offer-letter-agent.git
   cd offer-letter-agent

2. **Install dependencies**:
  pip install -r requirements.txt

3. **Set up environment**:
GEMINI_API_KEY=your_gemini_key_here

4. **Run the app**:
  streamlit run app.py
