from dotenv import load_dotenv
load_dotenv()

import base64
import os
import json
import re
from groq import Groq

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def encode_image(image_path):
    if not image_path or not os.path.exists(image_path):
        return None

    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def analyze_medical_report(image_path):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return {"error": "Server configuration error"}

    if not image_path:
        return {"error": "Please upload a report image"}

    try:

        encoded = encode_image(image_path)

        if not encoded:
            return {"error": "Unable to read image"}

        client = Groq(api_key=api_key)

        prompt = """
        Extract medical values from this report.

        Find if present:

        Blood Pressure (systolic and diastolic)
        Blood Sugar
        Cholesterol

        Return JSON ONLY like this:

        {
        "systolic_bp": number,
        "diastolic_bp": number,
        "blood_sugar": number,
        "cholesterol": number
        }

        If any value is missing return null.
        """

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded}"}
                    }
                ]
            }
        ]

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )

        if not response.choices:
            return {"error": "Could not analyze report"}

        content = response.choices[0].message.content

        # extract JSON safely
        match = re.search(r"\{.*\}", content, re.DOTALL)

        if match:
            return json.loads(match.group())

        return {"error": "Could not parse report values"}

    except Exception as e:
        print("Report Analyzer Error:", e)
        return {"error": "Error analyzing report"}