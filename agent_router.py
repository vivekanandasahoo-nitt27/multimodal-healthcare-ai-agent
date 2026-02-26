def classify_intent(user_message: str):
    if not user_message:
        return "chat"

    msg = user_message.lower()

    emergency_keywords = [
        "severe pain",
        "bleeding",
        "unconscious",
        "emergency",
        "chest pain",
        "difficulty breathing",
        "blood"
    ]

    report_keywords = ["report", "summary", "pdf"]

    if any(k in msg for k in emergency_keywords):
        return "emergency"

    if any(k in msg for k in report_keywords):
        return "report"

    return "chat"