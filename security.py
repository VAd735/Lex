import re
PHONE_RE = re.compile(r"(\+?\d[\d\-\s]{6,}\d)")
EMAIL_RE = re.compile(r"[\w\.-]+@[\w\.-]+")

def scrub_text(text: str) -> str:
    t = PHONE_RE.sub("[PHONE]", text)
    t = EMAIL_RE.sub("[EMAIL]", t)
    return t
