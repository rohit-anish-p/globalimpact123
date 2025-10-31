import streamlit as st
import google.generativeai as genai
import os

# --- THIS IS THE MOST IMPORTANT PART ---
# This is the "brain" or "persona" of your AI.
# The user's prompt is attached to this one.
SYSTEM_PROMPT = """
You are a 'Carbon Savings Simulator' bot for users in India.
Your goal is to answer a user's 'what-if' question about a lifestyle change.

Your response MUST be formatted as follows (use Markdown):
1.  **Your Estimated Annual Impact:** A clear, one-sentence answer.
2.  **Annual CO2 Savings:** A bolded estimate in `kg CO2 / year`.
3.  **Relatable Analogy:** A simple, encouraging analogy (e.g., "That's like planting X trees," "This has the same impact as charging X smartphones," "That saves the emissions of a X km car ride.").

RULES:
- Base your estimations on common data for India where possible (e.g., Indian energy grid emissions, local travel data).
- Use simple, encouraging, and non-judgmental language.
- If a question is too complex, unanswerable, or unrelated (e.g., "what is the moon?"), politely decline and ask for a lifestyle question (e.g., about food, transport, energy, or shopping).
"""

# --- Function to get API key and call the AI ---
def get_ai_response(user_question):
    """
    Calls the Gemini API with the system prompt and user question.
    """
    try:
        # Try to get the API key from Streamlit's secrets
        api_key = st.secrets.get("GEMINI_API_KEY")

        if not api_key:
            st.error("API Key not found. Please set your GEMINI_API_KEY in Streamlit secrets.")
            return None
        
        genai.configure(api_key=api_key)
        
        # Create the model
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Combine the system prompt and user question
        full_prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {user_question}"
        
        # Generate content
        response = model.generate_content(full_prompt)
        return response.text

    except Exception as e:
        st.error(f"An error occurred while contacting the AI: {e}")
        return None

# --- Streamlit App UI ---
st.set_page_config(layout="centered", page_title="Carbon Simulator")

# Header
st.title("🌍 'What-If' Carbon Simulator")
st.markdown("Curious about your climate impact? Ask a question about a lifestyle change to see the potential carbon savings!")

st.markdown("---")

# Example questions to guide the user
st.subheader("Example Questions to Ask:")
st.caption("- What if I stop eating beef and switch to chicken?")
st.caption("- What if I switch from my petrol car to a bus for my 20km daily commute?")
st.caption("- What if I switch my 5 most-used bulbs to LEDs?")
st.caption("- What if I take 5-minute showers instead of 10-minute ones?")

st.markdown("---")

# User input
user_question = st.text_input(
    "**Your 'What-If' Question:**", 
    placeholder="e.g., What if I stop using plastic bags?"
)

if st.button("Calculate My Impact"):
    if user_question:
        with st.spinner("Simulating your impact... 🌱"):
            ai_response = get_ai_response(user_question)
            
            if ai_response:
                st.markdown("### 💡 Your Simulated Impact")
                st.markdown(ai_response) # The AI's response is already formatted
    else:
        st.warning("Please ask a question first!")