from dotenv import load_dotenv
load_dotenv()

import base64
import os
from groq import Groq

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def encode_image(image_path):
    if not image_path or not os.path.exists(image_path):
        return None
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_image_with_query(query, image_path):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Server configuration error. Please try later."

    if not image_path:
        return "Please upload a medical image."

    try:
        encoded = encode_image(image_path)
        if not encoded:
            return "Unable to read the image."

        client = Groq(api_key=api_key)

        messages = [{
            "role": "user",
            "content": [
                {"type": "text", "text": query},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
                }
            ]
        }]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        if not response.choices:
            return "I could not analyze the image. Please try again."

        return response.choices[0].message.content

    except Exception as e:
        print("Groq Vision Error:", e)
        return "An error occurred while analyzing the image."
