
from openai_client import compare_images

def analyze_graphs(image1_path, image2_path, status,start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None, df1=None, df2=None):
    try:
        summary = compare_images(
            image1_path,
            image2_path,
            df1=df1,
            df2=df2,
            status=status,
            start_date_1=start_date_1,
            end_date_1=end_date_1,
            start_date_2=start_date_2,
            end_date_2=end_date_2
        )
        return summary
    except Exception as e:
        return f"Error: {e}"


# import streamlit as st
# from PIL import Image
# import google.generativeai as genai
# from dotenv import load_dotenv
# import os
# import pytesseract
# from PIL import Image
# from openai_client import compare_images
# load_dotenv()

# api_key = os.getenv("AZURE_OPENAI_API_KEY")
# endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
# deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
# model = os.getenv("AZURE_OPENAI_MODEL_NAME")
# version = os.getenv("AZURE_OPENAI_API_VERSION")


# def analyze_graphs(image1_path, image2_path, start_date_1=None, end_date_1=None, start_date_2=None, end_date_2=None):
#     try:
#         summary = compare_images(
#             image1_path,
#             image2_path,
#             start_date_1=start_date_1,
#             end_date_1=end_date_1,
#             start_date_2=start_date_2,
#             end_date_2=end_date_2
#         )
#         return summary
#     except Exception as e:
#         return f"Error: {e}"

