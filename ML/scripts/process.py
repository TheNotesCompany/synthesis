import re

def extract_concepts(text):
    # concepts like: "Neural Networks", "System Design", etc.
    pattern = r"\b[A-Z][A-Za-z0-9 ]{2,}\b"
    candidates = re.findall(pattern, text)
    return list(set(candidates))

def extract_questions(text):
    pattern = r"(?:What|Why|How|Explain|Define|Describe|List|When|Where)[^?]+\?"
    return list(set(re.findall(pattern, text, flags=re.IGNORECASE)))
