from dotenv import load_dotenv
load_dotenv()

from groq import Groq

def transcribe_with_groq(audio_filepath, stt_model="whisper-large-v3"):
    if not audio_filepath:
        return ""

    try:
        client = Groq()
        with open(audio_filepath, "rb") as audio:
            result = client.audio.transcriptions.create(
                model=stt_model,
                file=audio,
                language="en"
            )
        return result.text

    except Exception as e:
        print("Groq STT Error:", e)
        return ""
