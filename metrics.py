import re

def evaluate_claims(text):
    text = text.lower()

    correct = len(re.findall(r'\bcorrect\b', text))
    incorrect = len(re.findall(r'\bincorrect\b', text))

    total = correct + incorrect

    if total == 0:
        return {
            "accuracy": 0,
            "hallucination_rate": 1,
            "risk": "HIGH"
        }

    accuracy = correct / total
    hallucination = incorrect / total

    if hallucination < 0.2:
        risk = "LOW"
    elif hallucination < 0.5:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "accuracy": round(accuracy, 2),
        "hallucination_rate": round(hallucination, 2),
        "risk": risk
    }