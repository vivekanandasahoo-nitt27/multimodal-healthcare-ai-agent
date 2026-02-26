import os
import json
from datetime import date
from groq import Groq
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"


def format_medical_report_with_groq(doctor_response: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"observation": doctor_response, "medication": "Consult a doctor."}

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
Return ONLY valid JSON.
No markdown. No explanation.

Format:
{{"observation": "...", "medication": "..."}}

Doctor Response:
{doctor_response}
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        if not response.choices:
            raise ValueError("Empty Groq response")

        content = response.choices[0].message.content.strip()

        if content.startswith("```"):
            content = content.split("```")[1].strip()

        data = json.loads(content)

        return {
            "observation": data.get("observation", doctor_response),
            "medication": data.get("medication", "Consult a doctor.")
        }

    except Exception as e:
        print("Groq report formatting error:", e)
        return {"observation": doctor_response, "medication": "Consult a doctor."}


def generate_handwritten_medical_pdf(observation: str, medication: str) -> str:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(BASE_DIR, "medical_report.pdf")

    FONT_PATH = os.path.join(BASE_DIR, "fonts", "DoctorHandwriting.ttf")
    SIGNATURE_PATH = os.path.join(BASE_DIR, "assets", "signature.jpeg")

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    if os.path.exists(FONT_PATH):
        pdfmetrics.registerFont(TTFont("Handwriting", FONT_PATH))
        body_font = "Handwriting"
    else:
        body_font = "Helvetica"

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "Medical Observation Report")

    c.setFont("Helvetica", 10)
    c.drawString(50, height - 70, f"Date: {date.today()}")

    c.setFont(body_font, 12)
    text = c.beginText(50, height - 120)
    text.textLine("Observation:")
    text.textLines(observation)
    c.drawText(text)

    text = c.beginText(50, height - 300)
    text.textLine("Medication:")
    text.textLines(medication)
    c.drawText(text)

    c.setFont("Helvetica", 8)
    c.drawString(
        50, 150,
        "This AI-generated report is for educational purposes only. "
        "Consult a licensed medical professional."
    )

    if os.path.exists(SIGNATURE_PATH):
        c.drawImage(SIGNATURE_PATH, 50, 100, width=140, height=45)

    c.save()
    return output_path


def create_medical_report(doctor_response: str) -> str:
    structured = format_medical_report_with_groq(doctor_response)
    return generate_handwritten_medical_pdf(
        structured["observation"],
        structured["medication"]
    )
