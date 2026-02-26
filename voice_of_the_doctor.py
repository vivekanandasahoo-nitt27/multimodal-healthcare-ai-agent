import os
from elevenlabs.client import ElevenLabs
from elevenlabs import save

def text_to_speech_with_elevenlabs(text, output_path="doctor_voice.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key or not text:
        return None

    try:
        client = ElevenLabs(api_key=api_key)

        audio = client.text_to_speech.convert(
            voice_id="21m00Tcm4TlvDq8ikWAM",
            model_id="eleven_turbo_v2_5",
            text=text
        )

        save(audio, output_path)
        return output_path

    except Exception as e:
        print("ElevenLabs Error:", e)
        return None
