from dotenv import load_dotenv,find_dotenv
from transformers import pipline 
load_dotenv(find_dotenv())

def text2image(text):
    text_to_image = pipline("Text-to-Image",model= )