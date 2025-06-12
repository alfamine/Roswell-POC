import streamlit as st
import openai
import time

# Set OpenAI API key from secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page settings
st.set_page_config(page_title="Roswell-POC", page_icon="📘")
st.title("📘 Roswell-POC – Ordinance Chatbot")
st.subheader("Ask about Roswell, GA Code of Ordinances")
st.markdown("💼 *Powered by OpenAI + Alfentra*")

# Sidebar branding
st.sidebar.markdown("## 🏛️ AI Ordinance Assistant")
st.sidebar.markdown("Welcome to **Roswell-POC**, an AI-powered demo trained on the Code of Ordinances for the City of Roswell, GA.")
st.sidebar.markdown("*Built and branded by Alfentra for municipal chatbot use cases.*")

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

# User input box
question = st.text_input("🔍 What do you want to know?", placeholder="e.g., What is the fine for dog violations?")

# Run on submit
if question:
    now = time.time()
    wait_time = 15  # seconds between requests

    if now - st.session_state.last_query_time < wait_time:
        st.warning("⏳ Please wait 15 seconds between questions to avoid hitting limits.")
    else:
        st.session_state.last_query_time = now
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a helpful city ordinance assistant. Use this context only:\n\n{document_context}"},
                        {"role": "user", "content": question}
                    ],
                    temperature=0.4,
                    max_tokens=300
                )

                # Safely extract response
                answer = response.choices[0].message.content
                if answer.strip():
                    st.success(answer)
                else:
                    st.warning("⚠️ Received empty response. Try rephrasing your question.")
                    st.text("🔎 Raw API response:")
                    st.json(response.model_dump())

            except openai.RateLimitError:
                st.error("⚠️ Too many requests. Please wait and try again.")
            except openai.AuthenticationError:
                st.error("❌ Invalid or expired API key.")
            except Exception as e:
                st.error("⚠️ Unexpected error occurred.")
                st.text("🔎 Raw API response (if any):")
                st.json(response.model_dump())
