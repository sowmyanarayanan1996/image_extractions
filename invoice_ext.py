from dotenv import load_dotenv
import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

load_dotenv()

# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
GOOG_API_KEY ="AIzaSyAHIrXrwJ1y1uHSJCLN2WfvIEcEyWkih98"
genai.configure(api_key = GOOG_API_KEY)
model = genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,prompt):
    response= model.generate_content([input,image[0],prompt])
    return response.text

def input_image(upload_file):
    if upload_file is not None:
        bytes_data = upload_file.getvalue()

        image_parts = [
            {
                "mime_type": upload_file.type,  # Corrected typo from "mine_type" to "mime_type"
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("status code: 400")




st.set_page_config(page_title="Invoice extraction")

st.header("Invoice extraction Gemini LLM")
input= st.text_area("input promppt: ",key="input")
upload_file = st.file_uploader("Choose an image... ",type=["jpeg","jpg","png","pdf"])
image=""

if upload_file is not None:
    image= Image.open(upload_file)
    st.image(image,caption="uploaded image successfully",use_column_width=True)


submit = st.button("Submit")

input_prompt = """
you are an expert in understanding invoices. We will upload a image as invoice and you will have to answer any questions based on the uploaded invoice image.
"""

if submit:   
    image_data = input_image(upload_file)
    respone = get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is :")
    st.write(respone)
