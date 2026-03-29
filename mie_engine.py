import google.generativeai as genai
import streamlit as st
import json

def get_gemini_client():
    """Initializes the Gemini API client using Streamlit secrets."""
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
        if not api_key or api_key == "PASTE_YOUR_GEMINI_API_KEY_HERE":
            return None
        genai.configure(api_key=api_key)
        return genai.GenerativeModel('gemini-2.0-flash')
    except Exception as e:
        return None

def diagnose_mistake(question_text: str, correct_answer: str, student_attempt: str):
    """
    Uses Gemini PedCoT (Pedagogical Chain-of-Thought) to analyze a student's answer
    and categorize their mistake.
    """
    model = get_gemini_client()
    if not model:
        return {
            "error": "API Key missing or invalid.",
            "diagnosis": "Unable to diagnose.",
            "error_category": "Unknown",
            "pedagogical_advice": "Please configure your GEMINI_API_KEY in .streamlit/secrets.toml"
        }

    prompt = f"""
    You are an expert Math Tutor AI. Your goal is to analyze a student's incorrect math attempt 
    and identify the core "thinking mistake" behind it.

    Follow this Pedagogical Chain-of-Thought (PedCoT) process:
    1. Understand the mathematical principle being tested.
    2. Reconstruct the steps the student took based on their attempt.
    3. Identify where they deviated from the correct logical path.
    4. Categorize the mistake strictly into one of three categories:
       - Factual: They misremembered a fact (e.g. 7 * 8 = 54 instead of 56).
       - Procedural: They messed up the order of operations or a specific algorithm step (e.g. subtracting instead of adding).
       - Conceptual: They fundamentally misunderstand the mathematical principle (e.g. treating decimal places like whole numbers).

    Input Data:
    - Question: {question_text}
    - Correct Answer: {correct_answer}
    - Student Attempt: {student_attempt}

    Respond IN STRICT JSON FORMAT with exactly these keys:
    {{
      "diagnosis": "A concise 1-2 sentence explanation of exactly what the student did wrong.",
      "error_category": "Factual | Procedural | Conceptual | None",
      "pedagogical_advice": "A 1-sentence hint you would give the student to help them realize their mistake without just giving them the answer."
    }}
    """

    try:
        response = model.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        # Parse the JSON response
        result = json.loads(response.text)
        return result
    except Exception as e:
        return {
            "error": str(e),
            "diagnosis": "Failed to connect to AI engine.",
            "error_category": "API Error",
            "pedagogical_advice": "Please check your network connection and API limits."
        }
