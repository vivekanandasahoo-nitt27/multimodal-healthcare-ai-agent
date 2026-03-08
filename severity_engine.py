def classify_bp(sys, dia):

    if sys < 120 and dia < 80:
        return "🟢 Normal"
    elif sys < 130:
        return "🟡 Elevated"
    elif sys < 140:
        return "🟠 Hypertension Stage 1"
    else:
        return "🔴 Hypertension Stage 2"


def classify_sugar(val):

    if val < 100:
        return "🟢 Normal"
    elif val < 126:
        return "🟡 Prediabetes"
    else:
        return "🔴 Diabetes"


def classify_chol(val):

    if val < 200:
        return "🟢 Desirable"
    elif val < 240:
        return "🟡 Borderline"
    else:
        return "🔴 High Cholesterol"