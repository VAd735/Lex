from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_DIR = "my_friend_ft"

tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
model = AutoModelForCausalLM.from_pretrained(MODEL_DIR, device_map="auto")

while True:
    user = input("You: ")
    if user.lower() == "exit":
        break

    prompt = f"User: {user}\nAssistant:"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        out = model.generate(
            **inputs,
            max_length=200,
            temperature=0.7,
            pad_token_id=tokenizer.eos_token_id
        )

    print("AI:", tokenizer.decode(out[0], skip_special_tokens=True))
    print()
