import streamlit as st

from openai import OpenAI

st.title("Streamlit OpenAI chat")

user_api_key = st.text_input("Enter your OpenAI API key", type="password")

user_prompt = st.text_input("Enter your prompt")

if user_api_key:
    client = OpenAI(api_key=user_api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a helpful assistant"},
            {"role": "user", "content": user_prompt}
            ],
        )
        st.write("OpenAI Response:")
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"An error occured: {e}")
        # st.stop()
else:
    st.write("Please enter your OpenAI API key to continue")

