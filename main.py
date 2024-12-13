import streamlit as st
import os
import google.generativeai as genai
from API_KEY import api_key
from PIL import Image

os.environ["GOOGLE_API_KEY"] = api_key

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

model = genai.GenerativeModel("gemini-1.5-flash")

def get_gemini_response(input, image,prompt):
    response = model.generate_content([input,image,prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()

        image_parts = {
        "mime_type":uploaded_file.type,
        "data":bytes_data
        }
        return image_parts
    else:
        raise FileNotFoundError("No File Uploaded")

st.set_page_config(page_title="MultiLanguage Invoice Extractor")

st.header("Talk with Your Invoice")

input = st.text_input("Input Prompt",key="input")
uploaded_file = st.file_uploader("Choose an Image...",type=["jpeg","jpg","png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image,caption="Uploaded Image",use_container_width=True)

submit = st.button("Tell me about the invoice") 

input_prompt = """
You are an expert in understanding invoices. We will upload a image as invoice
and you willhave to answer any questions based on the uplaoded invoice image
"""

if submit:
    image_data = input_image_setup(uploaded_file)
    response = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is:")
    st.write(response)