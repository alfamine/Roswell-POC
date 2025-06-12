import streamlit as st
import openai

# Page config
st.set_page_config(page_title="AlfentraBot", page_icon="🤖")
st.title("🤖 AlfentraBot – Your Ordinance Assistant")
st.subheader("Ask questions about Roswell, GA Code of Ordinances")
st.markdown("💼 *Powered by Alfentra – Remote IT, Real People.*")

# Sidebar branding
st.sidebar.image("https://alfentra.com/wp-content/uploads/2024/04/AlfentraLogo.png", width=200)
st.sidebar.markdown("**Secure, AI-Powered Support**")
st.sidebar.markdown("*Built with OpenAI + Streamlit*")

# OpenAI API Key input
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Instructions
st.info("💡 Example: *What are the animal control rules in Roswell?*")

# Input box
user_question = st.text_input("Your question:")

# PDF context (simplified for demo)
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

if user_question:
    with st.spinner("Thinking..."):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are an ordinance assistant bot. Use the document below to answer questions:\n\n{document_context}"},
                {"role": "user", "content": user_question}
            ],
            max_tokens=300,
            temperature=0.4
        )
        answer = response['choices'][0]['message']['content']
        st.success(answer)
