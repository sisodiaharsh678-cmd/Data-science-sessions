import streamlit as st
from ollama import chat

st.title("Language Translator")

text = st.text_input(
    "Enter English Text"
)

if st.button("Translate"):

    prompt = f"""
    Translate to Hindi:

    {text}
    """

    response = chat(
        model="llama3",
        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ]
    )

    st.write(response["message"]["content"])