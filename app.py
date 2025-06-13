import streamlit as st
import openai
from PIL import Image
import time

# Set OpenAI API key from secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page settings
st.set_page_config(page_title="Roswell-POC", page_icon="📘")
logo = Image.open("IGT Logo.png")
st.logo(logo, width=180)
st.title("📘 Roswell-POC – Chatbot")
st.subheader("Ask about Roswell, GA Code of Ordinances")
st.markdown("💼 *Powered by OpenAI + InfoGlobalTech*")

# Sidebar branding
st.sidebar.markdown("## 🏛️ AI Ordinance Assistant")
st.sidebar.markdown("Welcome to **Roswell-POC**, an AI-powered demo trained on the Code of Ordinances for the City of Roswell, GA.")
st.sidebar.markdown("*Built and branded by InfoGlobalTech for municipal chatbot use cases.*")

# Sample ordinance content from PDF
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

# Track last query to prevent spamming
if "last_query_time" not in st.session_state:
    st.session_state.last_query_time = 0

# User input
question = st.text_input("🔍 What do you want to know?", placeholder="e.g., What is the fine for dog violations?")

# Handle query
if question:
    now = time.time()
    wait_time = 15  # seconds

    if now - st.session_state.last_query_time < wait_time:
        st.warning("⏳ Please wait 15 seconds between questions to avoid hitting limits.")
    else:
        st.session_state.last_query_time = now
        with st.spinner("Thinking..."):
            try:
                # Using gpt-3.5-turbo-instruct instead of chat model
                response = client.completions.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt=f"You are a helpful assistant for Roswell city ordinances. Use the following context to answer:\n\n{document_context}\n\nUser question: {question}",
                    temperature=0.4,
                    max_tokens=300
                )

                answer = response.choices[0].text.strip()
                if answer:
                    st.success(answer)
                else:
                    st.warning("⚠️ No answer generated. Try rephrasing.")
                    st.text("Raw response:")
                    st.json(response.model_dump())

            except openai.RateLimitError:
                st.error("⚠️ Too many requests. Please wait and try again.")
            except openai.AuthenticationError:
                st.error("❌ Invalid or expired API key.")
            except Exception as e:
                st.error("⚠️ Unexpected error occurred.")
                st.text("🔎 Raw response (if any):")
                st.json(response.model_dump())
