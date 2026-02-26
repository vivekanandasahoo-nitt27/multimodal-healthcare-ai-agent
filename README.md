🩺 AI Doctor – Vision & Voice Enabled Medical Assistant

An end-to-end AI Doctor application that accepts patient voice input and medical images, analyzes them using state-of-the-art AI models, and responds with a human-like doctor’s voice.
The system is fully deployed on AWS EC2 and accessible via a Gradio web interface.

🚀 Live Deployment

Platform: AWS EC2

Status: ✅ Running in Production

Interface: Gradio Web UI

🧠 System Architecture Overview

Input → Processing → AI Reasoning → Voice Response

🎙️ Patient speaks through microphone

🖼️ Optional medical image upload

🧾 Speech-to-Text transcription

🤖 Multimodal LLM medical reasoning

🔊 Doctor-like voice output

🛠️ Tech Stack
Frontend / UI

Gradio (Web-based interactive UI)

Speech Processing

SpeechRecognition

PyAudio

FFmpeg

Whisper (via Groq API)

AI Models

Speech-to-Text: Whisper Large v3 (Groq)

Vision + Reasoning: LLaMA Vision Models

Text-to-Speech: ElevenLabs, gTTS

Backend

Python

Groq API

ElevenLabs API

Deployment

AWS EC2

Linux Server

Virtual Environment (venv)

Environment Variables (.env)

📂 Project Structure
doctor_ai/
│
├── gradio_app.py              # Main Gradio UI entry point
├── brain_of_the_doctor.py     # Vision + LLM reasoning logic
├── voice_of_the_patient.py   # Audio recording & transcription
├── voice_of_the_doctor.py    # Text-to-Speech generation
│
├── requirements.txt
├── .env                       # API keys (not committed)
├── README.md
└── venv/

🎙️ Voice of the Patient (Speech-to-Text)

File: voice_of_the_patient.py

Records patient voice using microphone

Converts audio to MP3

Transcribes speech using Groq Whisper Large v3

Outputs clean English text for reasoning

🧠 Brain of the Doctor (Vision + AI Reasoning)

File: brain_of_the_doctor.py

Encodes medical images (Base64)

Sends patient text + image to a vision-enabled LLM

Generates concise, doctor-like medical responses

Avoids AI disclaimers and markdown formatting

🔊 Voice of the Doctor (Text-to-Speech)

File: voice_of_the_doctor.py

Converts AI-generated medical text into voice

Supports:

ElevenLabs (realistic doctor voice)

gTTS (fallback option)

Outputs playable MP3 audio

🖥️ Gradio Web Interface

File: gradio_app.py

UI Components:

🎙️ Microphone audio input

🖼️ Image upload

📄 Transcribed patient text

🧠 Doctor’s medical response

🔊 Audio playback of doctor’s voice

Flow:
Audio + Image → AI Processing → Text Response → Voice Output

🔐 Environment Variables

Create a .env file:

GROQ_API_KEY=your_groq_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key


⚠️ Never commit .env to GitHub

🏗️ Deployment on AWS EC2
Steps Followed:

Launch EC2 (Ubuntu)

Install Python, FFmpeg, PortAudio

Create virtual environment

Install dependencies

Set environment variables

Run Gradio app

Expose port via Security Group

▶️ How to Run Locally
git clone <repo-url>
cd doctor_ai
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python gradio_app.py


App runs at:

http://127.0.0.1:7860

⚠️ Disclaimer

This project is built strictly for educational and learning purposes.
It does not replace professional medical advice.

📌 Key Highlights

Multimodal AI (Voice + Vision)

Realistic doctor voice responses

Production deployment on AWS EC2

Clean modular architecture

Resume & portfolio ready project