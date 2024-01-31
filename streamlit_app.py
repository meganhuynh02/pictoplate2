# Code refactored from https://docs.streamlit.io/knowledge-base/tutorials/build-conversational-apps

import streamlit as st
from openai import OpenAI

# create website sidebar
with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"

# create page header
st.header(':cook: PicToPlate', divider='rainbow')

#create page subheader
st.subheader("Welcome to PicToPlate! Cooking at home has never been easier.")

#introduction to product
st.markdown('PicToPlate is an innovation application that allows home chefs to input an image of ingredients \
            they have, and PicToPlate will return a list of recipes they can cook using what they already have. \
            To get started, follow the instructions below.')

#create page caption
st.caption(":shallow_pan_of_food: A cooking assistant powered by OpenAI LLM")

#default on screen message
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "What should we cook today? :yum:"}]

picture = st.camera_input("Take a picture of the ingredients you have")
if picture:
    st.image(picture)

uploaded_file = st.file_uploader("Or upload an existing picture")

if uploaded_file and not openai_api_key:
    st.info("Please add your OpenAI API key to continue.")

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    picture = st.camera_input("Take a picture of the ingredients you have")
    if picture:
        st.image(picture)

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(model="gpt-4-vision-preview", messages=st.session_state.messages)
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)