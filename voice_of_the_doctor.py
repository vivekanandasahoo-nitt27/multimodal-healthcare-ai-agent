import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def text_to_speech_with_elevenlabs(text, language="English", output_path="doctor_voice.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or not text:
        return None

    try:
        client = ElevenLabs(api_key=api_key)
        voice_map = {
            "English": "21m00Tcm4TlvDq8ikWAM",
            "Hindi": "21m00Tcm4TlvDq8ikWAM",
            "Tamil": "21m00Tcm4TlvDq8ikWAM",
            "Telugu": "21m00Tcm4TlvDq8ikWAM",
            "Odia": "21m00Tcm4TlvDq8ikWAM",
            "Bengali": "21m00Tcm4TlvDq8ikWAM",
            "Kannada": "21m00Tcm4TlvDq8ikWAM",
            "Malayalam": "21m00Tcm4TlvDq8ikWAM",
            "Marathi": "21m00Tcm4TlvDq8ikWAM",
            "Gujarati": "21m00Tcm4TlvDq8ikWAM"
        }

        voice_id = voice_map.get(language, "21m00Tcm4TlvDq8ikWAM")

        audio = client.text_to_speech.convert(
            voice_id=voice_id,
            model_id="eleven_turbo_v2_5",
            text=text
        )

        save(audio, output_path)
        return output_path

    except Exception as e:
        print("ElevenLabs Error:", e)
        return None
