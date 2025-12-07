import google.generativeai as genai
import json
from datetime import date

GOOGLE_API_KEY = "api_keyy"

def parse_expense_with_ai(user_text):
    """
    Sends the user's natural language text to Gemini and gets back structured JSON.
    """
    if not GOOGLE_API_KEY:
        return None, "API Key is missing in ai_helper.py"

    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash') 

    today = date.today()
    categories = "Food, Travel, Bills, Shopping, Other"

    prompt = f"""
    You are an API that converts natural language expense text into JSON.
    Current Date: {today}
    Valid Categories: {categories}

    Instructions:
    1. Extract the amount, category, date, and description.
    2. If no date is mentioned, use Current Date.
    3. If the category doesn't match the Valid Categories list strictly, pick the closest one or use 'Other'.
    4. Return ONLY a JSON object. Do not write markdown or explanations.

    User Input: "{user_text}"
    
    Output Format:
    {{
        "date": "YYYY-MM-DD",
        "category": "String",
        "amount": Float,
        "description": "String"
    }}
    """

    try:
        response = model.generate_content(prompt)
        # Clean up the text to ensure it's pure JSON (sometimes AI adds ```json blocks)
        cleaned_text = response.text.strip().replace("```json", "").replace("```", "")
        parsed_data = json.loads(cleaned_text)
        return parsed_data, None
    except Exception as e:
        return None, f"AI Error: {str(e)}"