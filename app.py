from dotenv import load_dotenv
load_dotenv()

import os
import streamlit as st
import google.generativeai as genai
from PIL import Image

os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

with open("index.html", "r") as html_file:
    st.markdown(html_file.read(), unsafe_allow_html=True)

st.header("Disease Classification")

def generate_response(input, image, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input, image[0], prompt])
    return response.text

def get_gemini_response(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type" : uploaded_file.type,
                "data" : bytes_data

            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file Found")


input = st.text_input("Give the input on what you want?", key="input")
uploaded_file = st.file_uploader("Choose an Image to upload", type=["jpg","jpeg", "png"])
image = ""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Upload Image of Disease", use_column_width=True)

submit = st.button("Generate Response")


input_prompt = """You are great in understanding what disease it is. We will upload a image and You are 
required to understand what disease it is and describe about the disease accurately and provide medications and
preventions for the particular disease"""

if submit:
    image_data = get_gemini_response(uploaded_file)
    response = generate_response(input_prompt, image_data, input)
    st.subheader("The Response is")
    st.write(response)