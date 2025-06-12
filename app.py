import streamlit as st
import openai

# Set OpenAI key from Streamlit secrets
client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Page config
st.set_page_config(page_title="Roswell-POC", page_icon="📘")
st.title("📘 Roswell-POC – Ordinance Chatbot")
st.subheader("Ask about Roswell, GA Code of Ordinances")
st.markdown("💼 *Powered by OpenAI + Alfentra*")

# Sidebar branding
st.sidebar.markdown("**AI-powered City Ordinance Assistant**")
st.sidebar.markdown("*Built for demonstration purposes*")

# Sample ordinance content from PDF
document_context = """
Chapter 8. Health and Public Safety – Roswell Ordinances

Animal Control:
- No person shall own or harbor any animal which is a nuisance.
- All dogs must be vaccinated and tagged.
- Animal control officers may seize animals found violating these rules.
- Violation of these laws may lead to fines up to $500.

Emergency Services:
- The Emergency Management Director coordinates disaster response.
- Citizens must follow emergency directives from the city.
"""

# Get user input
question = st.text_input("Ask a question:")

# If a question is asked
if question:
    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Use only this context:\n\n{document_context}"},
                {"role": "user", "content": question}
            ],
            temperature=0.4,
            max_tokens=300
        )
        answer = response.choices[0].message.content
        st.success(answer)
