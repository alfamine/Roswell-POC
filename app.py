import streamlit as st
import openai
import time

# Set OpenAI API key from secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set page config
st.set_page_config(page_title="Roswell-POC", page_icon="📘")
st.title("📘 Roswell-POC – Ordinance Chatbot")
st.subheader("Ask about Roswell, GA Code of Ordinances")
st.markdown("💼 *Powered by OpenAI + Alfentra*")

# Sidebar branding
st.sidebar.markdown("## 🏛️ AI Ordinance Assistant")
st.sidebar.markdown("Welcome to **Roswell-POC**, an AI-powered demo assistant trained on the Code of Ordinances for the City of Roswell, GA.")
st.sidebar.markdown("*Built and branded by Alfentra for city use case demos.*")

# Sample ordinance document context
document_context = """
City of Roswell, GA – Code of Ordinances (Sample Excerpt)

Chapter 8: Health and Public Safety

Animal Control:
- No person shall own or harbor any animal which is a nuisance.
- All dogs must be vaccinated and tagged.
- Animal control officers may seize animals violating these rules.
- Violations may result in fines up to $500.

Emergency Services:
- The Emergency Management Director coordinates disaster response.
- Residents must follow all emergency orders during declared emergencies.

Noise Ordinance:
- Excessive noise between 10 PM and 6 AM is prohibited in residential areas.
"""

# Store last query time in session to avoid spamming
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = 0

# Input from user
question = st.text_input("🔍 What do you want to know?", placeholder="e.g., What is the fine for dog violations?")

# If question submitted
if question:
    now = time.time()
    wait_time = 15  # 15 seconds between queri_
