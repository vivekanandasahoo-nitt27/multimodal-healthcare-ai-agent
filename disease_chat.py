import os
from groq import Groq

MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

def disease_followup_chat(doctor_response, user_question, history):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "Server configuration error.", history

    try:
        client = Groq(api_key=api_key)

        prompt = f"""
Initial medical observation:
{doctor_response}

Conversation so far:
{history}

User question:
{user_question}

Rules:
- Explain disease
- Suggest precautions
- Suggest medication
"""

        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )

        if not response.choices:
            return "I could not answer that. Try again.", history

        answer = response.choices[0].message.content
        history.append({"question": user_question, "answer": answer})

        return answer, history

    except Exception as e:
        print("Groq Followup Error:", e)
        return "An error occurred. Please try again.", history
