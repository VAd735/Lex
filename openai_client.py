import os
import openai
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("MODEL_NAME", "gpt-4o-mini")

def chat_with_model(system_prompt, user_prompt, temperature=0.2, max_tokens=800):
    messages = [
        {"role":"system", "content": system_prompt},
        {"role":"user", "content": user_prompt}
    ]
    resp = openai.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens
    )
    return resp.choices[0].message.content
