import gradio as gr
from voice_of_the_patient import transcribe_with_groq
from brain_of_the_doctor import analyze_image_with_query
from voice_of_the_doctor import text_to_speech_with_elevenlabs
from doctor_report import create_medical_report
from disease_chat import disease_followup_chat

from database import init_db
from report_storage import save_report_for_user
from auth import create_user, authenticate_user
from report_storage import get_user_reports
from agent_router import classify_intent
from emergency_agent import build_emergency_response
from report_analyzer import analyze_medical_report
from severity_engine import classify_bp, classify_sugar, classify_chol
from health_metrics import save_metric, get_metric_history
import json
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

from who_rag import retrieve_who_context


SYSTEM_PROMPT = """
You have to act as a professional doctor i know you are not but this is for learning purpose
Whats in this image Do you find anything wrong with it medically
If you make a differential suggest some remedies for them
please give a brief descripting of the problem 
Important include the medication and medicine in oder for the patient
Donot add any numbers or special characters in your response
Your response should be in one long paragraph
Always answer as if you are answering a real person
Donot say In the image I see but say With what I see I think you have
Dont respond as an AI model or in markdown
Mimic an actual doctor not an AI bot
in last please ask the person for the consult a doctor and give wishesto get well soon
No preamble start your answer right away
"""


# --------------------------
# INITIAL PROCESS
# --------------------------

def signup(email, password):
    user = create_user(email, password)
    if not user:
        return None, "User exists"
    return user.id, "Signup success"


def login(email, password):
    user = authenticate_user(email, password)
    if not user:
        return None, "Invalid credentials"
    return user.id, "Login success"


def process_health_dashboard(report_image, user_id):

    result = analyze_medical_report(report_image)

    data = result
    if "error" in data:
        return data["error"], "", "", None, None, None

    sys = data.get("systolic_bp")
    dia = data.get("diastolic_bp")
    sugar = data.get("blood_sugar")
    chol = data.get("cholesterol")

    if not all([sys, dia, sugar, chol]):
        return "Extraction failed", "", "", None, None, None

    bp_status = classify_bp(sys, dia)
    sugar_status = classify_sugar(sugar)
    chol_status = classify_chol(chol)

    save_metric(user_id, "blood_pressure", f"{sys}/{dia}")
    save_metric(user_id,"blood_sugar",sugar)
    save_metric(user_id,"cholesterol",chol)

    bp_rows = get_metric_history(user_id,"blood_pressure")
    sugar_rows = get_metric_history(user_id,"blood_sugar")
    chol_rows = get_metric_history(user_id,"cholesterol")
    
    bp_rows = sorted(bp_rows, key=lambda x: x.created_at)
    sugar_rows = sorted(sugar_rows, key=lambda x: x.created_at)
    chol_rows = sorted(chol_rows, key=lambda x: x.created_at)

    
    if len(bp_rows) < 2:
        bp_history = None
    else:
        bp_history = pd.DataFrame([
            {"date": r.created_at, "value": int(r.value.split("/")[0])}
            for r in bp_rows
        ])

    
    if len(sugar_rows) < 2:
        sugar_history = None
    else:
        sugar_history = pd.DataFrame([
            {"date": r.created_at, "value": int(r.value)}
            for r in sugar_rows
        ])

    if len(chol_rows) < 2:
        chol_history = None
    else:
        chol_history = pd.DataFrame([
            {"date": r.created_at, "value": int(r.value)}
            for r in chol_rows
        ])

    bp_card = f"""
    ### Blood Pressure
    {bp_status}

    {sys}/{dia} mmHg
    """
    sugar_card = f"""
    ### Blood Sugar
    {sugar_status}

    {sugar} mg/dL
    """
    chol_card = f"""
    ### Cholesterol
    {chol_status}

    {chol} mg/dL
    """
    

    return bp_card, sugar_card, chol_card, bp_history, sugar_history, chol_history


def process_initial(audio_filepath, image_filepath, language, state):
    state = state or []

    if not audio_filepath and not image_filepath:
        return "", state, None, state

    patient_text = transcribe_with_groq(audio_filepath)
    if not patient_text.strip():
        patient_text = f"Analyze this medical image. Respond in {language}."

    who_context = retrieve_who_context(patient_text)
    enhanced_prompt = f"""
    {SYSTEM_PROMPT}
    IMPORTANT:
    Respond ONLY in {language}.
    All explanations, medical advice, and instructions must be in {language}.

    

    Use established emergency medical care standards internally when forming your response.
    Do not mention WHO explicitly.

    Relevant Emergency Guidelines:
    {who_context}

    Patient says: {patient_text}
    """

    if image_filepath:
        doctor_response = analyze_image_with_query(enhanced_prompt, image_filepath)
    else:
        doctor_response = "Please upload an image."

    audio_path = text_to_speech_with_elevenlabs(doctor_response, language)

    state = [
        {"question": patient_text, "answer": doctor_response}
    ]

    chatbot_history = [
    {"role": "user", "content": patient_text},
    {"role": "assistant", "content": doctor_response},
]

    return "", chatbot_history, audio_path, state


# --------------------------
# FOLLOW-UP CHAT
# --------------------------
def state_to_chatbot(state):
    messages = []
    for item in state:
        messages.append({"role": "user", "content": item["question"]})
        messages.append({"role": "assistant", "content": item["answer"]})
    return messages





def continue_chat(user_message, state, user_id):
    if not state:
        return "", [], state

    intent = classify_intent(user_message)

    # ---- REPORT INTENT ----
    if intent == "report":
        return "", [(user_message, "You can generate a report using the Generate Report button.")], state

    # ---- EMERGENCY INTENT ----
    if intent == "emergency":
        lat = 10.7595  
        lng = 78.8137   

        messages = build_emergency_response(lat, lng)

    # Extract assistant emergency text
        emergency_text = "\n".join(
            [m["content"] for m in messages if m["role"] == "assistant"]
        )

        # Save into memory state
        state.append({
            "question": user_message,
            "answer": emergency_text
        })

        return "", state_to_chatbot(state), state
    # ---- NORMAL CHAT ----
    initial_response = state[0]["answer"]
    history_only = state[1:]

    answer, updated_history = disease_followup_chat(
        doctor_response=initial_response,
        user_question=user_message,
        history=history_only
    )

    state = (
        [state[0]] +
        updated_history +
        [{"question": user_message, "answer": answer}]
    )

    chatbot_history = []
    for e in state:
        chatbot_history.append({"role": "user", "content": e["question"]})
        chatbot_history.append({"role": "assistant", "content": e["answer"]})

    return "", chatbot_history, state

# --------------------------
# FINAL REPORT
# --------------------------
def generate_final_report(state, user_id):
    if not state:
        return None
    
    if not user_id:
        return None 

    full_text = "\n".join(
        f"Patient: {e['question']}\nDoctor: {e['answer']}"
        for e in state
    )

    pdf_path = create_medical_report(full_text)

    saved_path = save_report_for_user(user_id, pdf_path)

    return saved_path


def load_reports(user_id):
    if not user_id:
        return []

    return get_user_reports(user_id)


init_db()
# ===============================
# GRADIO UI
# ===============================
with gr.Blocks(title="AI Doctor with Vision, Voice, and Chat") as demo:
    gr.Markdown("# 🩺 AI Doctor with Vision, Voice, and Chat")

    session_state = gr.State([])
    user_state = gr.State(None)
    with gr.Tabs():
        with gr.Tab("🔐 Login"):

            gr.Markdown("## Login / Signup")

            email_input = gr.Textbox(label="Email")
            password_input = gr.Textbox(label="Password", type="password")

            signup_btn = gr.Button("Signup")
            login_btn = gr.Button("Login")

            login_status = gr.Markdown("")
            
        
    
        with gr.Tab("🩺 Consultation"):

            with gr.Row():
                language_selector = gr.Dropdown(
                choices=[
                    "English","Hindi","Tamil","Telugu","Odia",
                    "Bengali","Kannada","Malayalam","Marathi","Gujarati"
                ],
                value="English",
                label="Patient Language"
                )

                audio_input = gr.Audio(
                    sources=["microphone", "upload"],
                    type="filepath",
                    label="Patient Voice (Upload or Record)"
                )
                image_input = gr.Image(type="filepath", label="Upload Image")
                submit_btn = gr.Button("Submit Initial")

            chatbot = gr.Chatbot(label="Doctor Chat")
            user_message = gr.Textbox(label="Type your message here")
            send_btn = gr.Button("Send Message")

            audio_output = gr.Audio(label="Doctor Voice", autoplay=True)

            final_report_btn = gr.Button("Generate Final Report")
            report_file = gr.File(label="Download Final Medical Report (PDF)")


    
        with gr.Tab("📊 My Health Dashboard"):
            

                

            # Upload report
            report_upload = gr.Image(type="filepath", label="Upload Medical Report")
            analyze_report_btn = gr.Button("Analyze Report")

            gr.Markdown("---")

            # Health metrics row
            with gr.Row():
                bp_card = gr.Markdown("### Blood Pressure\nNo Data")
                sugar_card = gr.Markdown("### Blood Sugar\nNo Data")
                chol_card = gr.Markdown("### Cholesterol\nNo Data")

            gr.Markdown("### Health Trends")
            
            with gr.Row():
                bp_graph = gr.LinePlot(
                    x="date",
                    y="value",
                    title="Blood Pressure Trend"
                )

                sugar_graph = gr.LinePlot(
                    x="date",
                    y="value",
                    title="Blood Sugar Trend"
                )

                chol_graph = gr.LinePlot(
                    x="date",
                    y="value",
                    title="Cholesterol Trend"
                )
            gr.Markdown("---")


            

            gr.Markdown("## Previous Medical Reports")

            load_reports_btn = gr.Button("Load My Reports")
            reports_list = gr.Files(label="Your Previous Reports")
    
    


    
    signup_btn.click(
    fn=signup,
    inputs=[email_input, password_input],
    outputs=[user_state, login_status]
)

    login_btn.click(
        fn=login,
        inputs=[email_input, password_input],
        outputs=[user_state, login_status]
    )
    
    submit_btn.click(
        fn=process_initial,
        inputs=[audio_input, image_input, language_selector, session_state],
        outputs=[user_message, chatbot, audio_output, session_state],
        api_name=False
    )

    send_btn.click(
        fn=continue_chat,
        inputs=[user_message, session_state, user_state],
        outputs=[user_message, chatbot, session_state],
        api_name=False
    )

    final_report_btn.click(
        fn=generate_final_report,
        inputs=[session_state,user_state],
        outputs=[report_file],
        api_name=False
    )
    
    load_reports_btn.click(
    fn=load_reports,
    inputs=[user_state],
    outputs=[reports_list]
    )
    analyze_report_btn.click(
    fn=process_health_dashboard,
    inputs=[report_upload, user_state],
    outputs=[
        bp_card,
        sugar_card,
        chol_card,
        bp_graph,
        sugar_graph,
        chol_graph
    ]
    )

demo.launch(
    server_name="127.0.0.1",
    server_port=7860,
    share=True
)
