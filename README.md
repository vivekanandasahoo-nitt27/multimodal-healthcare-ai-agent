# 🩺 AI Doctor — Multimodal Healthcare AI Agent with Emergency Assistance

An end-to-end **Multimodal Healthcare AI Agent** that understands patient voice, medical images, conversational context, and emergency situations.

The system performs medical reasoning, enables follow-up chat, generates structured medical reports, and provides emergency assistance by showing nearby hospitals with directions.

The application is containerized with Docker and deployable on cloud platforms such as AWS.

## Project development history:
https://github.com/vivekanandasahoo-nit27/multimodal-healthcare-ai-agent/commits/main

---

## 🚀 Live Deployment
* Live Server: http://44.197.103.98/
* Platform:  AWS EC2 ,Docker
* Status: ✅ Production Ready
* Interface: Gradio Web UI
* Architecture: Agent-based multimodal AI system

---

## 🧠 System Overview

Input → Agent Router → AI Reasoning → Response → Report / Emergency Support

### Flow

* 🎙️ Patient voice input
* 🖼️ Optional medical image
* 🧠 Multimodal reasoning (Vision + LLM)
* 💬 Follow-up conversational memory
* 📄 Medical report generation (PDF)
* 🚑 Emergency detection → Nearby hospitals + directions
* 🔊 Doctor-like voice response

---

## 🤖 Core Agents (Agentic Architecture)

### 1️⃣ Medical Reasoning Agent

Handles:

* Voice transcription
* Image understanding
* Doctor-style response generation

---

### 2️⃣ Conversation / Follow-up Agent

Maintains session memory and enables:

* Multi-turn medical chat
* Context-aware follow-ups
* Disease guidance

---

### 3️⃣ Report Agent

Generates structured medical PDF reports and stores them per user.

Features:

* Session summary
* Downloadable reports
* Report history

---

### 4️⃣ Emergency Agent ⭐

Detects emergency intent (e.g. bleeding, chest pain).

Provides:

* Nearby hospitals (Google Places API)
* Hospital phone numbers
* Google Maps directions links
* Location-based assistance

---

### 5️⃣ Agent Router ⭐

Classifies user intent:

* Normal medical chat
* Emergency
* Report request

Routes the request to the correct agent.

---

## 🛠️ Tech Stack

### Frontend / UI

* Gradio (agent UI)
* Chat interface with session state
* File + audio components

---

### Speech Processing

* Groq Whisper Large v3
* FFmpeg
* PyDub

---

### AI Models

* Vision Reasoning: LLaMA Vision models
* STT: Whisper (Groq)
* TTS: ElevenLabs

---

### Backend

* Python
* Agent-based architecture
* Groq API
* Google Maps API (Places + Directions)

---

### Database ⭐

* SQLAlchemy
* User authentication
* Report storage
* Report history

---

### Deployment

* Docker
* AWS EC2
* Environment variables (.env)

---

## 📂 Project Structure

```
doctor_ai/

├── app.py
├── agent_router.py
├── emergency_agent.py
├── disease_chat.py
├── doctor_report.py
├── report_storage.py
├── auth.py
├── database.py

├── brain_of_the_doctor.py
├── voice_of_the_patient.py
├── voice_of_the_doctor.py

├── requirements.txt
├── Dockerfile
├── .env
└── README.md
```

---

## 🔐 Authentication

New capability:

* Signup / Login
* User-specific reports
* Session-based experience

---

## 🚑 Emergency Assistance

When emergency is detected, the system automatically:

* Finds nearby hospitals
* Fetches phone numbers
* Generates Google Maps direction links
* Displays results inside chat UI

Uses:

* Google Places API
* Place Details API
* Maps Directions links

---

## 📄 Medical Report System

* Generates PDF summary
* Saves per user
* Users can load previous reports
* Portfolio-ready feature

---

## 🔊 Voice System

Patient → Speech → Text → AI reasoning → Doctor voice

Supports:

* ElevenLabs realistic voice
* Audio playback in UI

---

## 🔐 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_groq_api_key
ELEVEN_API_KEY=your_elevenlabs_api_key
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
```

⚠️ Never commit `.env` to GitHub

---

## 🐳 Docker Deployment

Build image:

```
docker build -t ai-doctor .
```

Run container:

```
docker run -p 7860:7860 --env-file .env ai-doctor
```

---

## 🏗️ AWS Deployment (High Level)

Steps:

1. Launch EC2 (Ubuntu)
2. Install Docker
3. Clone repository
4. Add `.env`
5. Build Docker image
6. Run container
7. Open port 7860 in security group

---

## ▶️ Run Locally

```
git clone <repo>
cd doctor_ai

python -m venv venv
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

App runs at:

```
http://127.0.0.1:7860
```

---

## 🧪 Key Highlights (Resume / Hackathon Strength)

* Agentic AI architecture (not a chatbot)
* Multimodal healthcare AI
* Emergency AI assistant
* Medical report generation
* User authentication + persistence
* Google Maps integration
* Dockerized deployment
* Production-ready architecture

---

## 🏆 Why This Project Is Advanced

Most projects stop at:

* Chatbot demo
* Single model demo

This project includes:

* Multi-agent system
* Memory
* Emergency reasoning
* Real-world API integration
* Full stack architecture
* Deployment ready

---

## ⚠️ Disclaimer

This project is built strictly for educational and research purposes and does not replace professional medical advice.
It work as a medical assistance and guide in emergency
---

## 👨‍💻 Author

Vivekananda Sahoo

Multimodal Healthcare AI Agent
Built for hackathons
