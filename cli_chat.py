import uuid
from memory import Memory
from openai_client import chat_with_model
from store import init_db, save_turn, save_feedback
from security import scrub_text

SYSTEM_PROMPT = "Ти — дружній асистент. Відповідай коротко та по суті."

def format_with_memory(user_query, mem_items):
    ctx = "\n".join([f"- {m['text']}" for m in mem_items])
    return f"Контекст:\n{ctx}\n\nПитання користувача: {user_query}"

def main():
    init_db()
    mem = Memory()
    session = str(uuid.uuid4())[:8]
    print(f"CLI chat started — session {session}. Напиши 'exit' щоб вийти.")
    last_turn_id = None

    while True:
        q = input("You: ").strip()
        if q.lower() in ("exit", "quit"):
            break
        if not q:
            continue

        q_clean = scrub_text(q)
        tid = save_turn(session, "user", q_clean)

        mem_relevant = mem.retrieve(q_clean, k=3)
        prompt = format_with_memory(q_clean, mem_relevant)
        ans = chat_with_model(SYSTEM_PROMPT, prompt)
        ans_clean = scrub_text(ans)
        atid = save_turn(session, "assistant", ans_clean)
        last_turn_id = atid

        print(f"FriendAI: {ans_clean}\n")

        fb = input("Оціни відповідь 1..5 (або Enter): ").strip()
        if fb.isdigit():
            save_feedback(last_turn_id, int(fb))

if __name__ == "__main__":
    main()
