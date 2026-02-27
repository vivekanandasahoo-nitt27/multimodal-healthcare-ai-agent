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

from dotenv import load_dotenv
load_dotenv()


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


def process_initial(audio_filepath, image_filepath, state):
    state = state or []

    if not audio_filepath and not image_filepath:
        return "", state, None, state

    patient_text = transcribe_with_groq(audio_filepath)
    if not patient_text.strip():
        patient_text = "Analyze this medical image."

    final_query = f"{SYSTEM_PROMPT}\nPatient says: {patient_text}"

    if image_filepath:
        doctor_response = analyze_image_with_query(final_query, image_filepath)
    else:
        doctor_response = "Please upload an image."

    audio_path = text_to_speech_with_elevenlabs(doctor_response)

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


    
        with gr.Tab("📄 Previous Reports"):

            gr.Markdown("## Previous Reports")

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
        inputs=[audio_input, image_input, session_state],
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

demo.launch(
    server_name="0.0.0.0",
    server_port=7860,
    share=False
)