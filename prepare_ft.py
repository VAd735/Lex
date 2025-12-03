import sqlite3, json
DB = "data/logs.db"

def build_pairs(limit=10000):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
    SELECT t1.text as user_text, t2.text as assistant_text
    FROM turns t1
    JOIN turns t2 ON t2.session_id = t1.session_id AND t2.timestamp > t1.timestamp
    WHERE t1.role='user' AND t2.role='assistant'
    ORDER BY t1.timestamp
    """)
    rows = c.fetchall()
    conn.close()
    for u, a in rows[:limit]:
        yield {"prompt": f"User: {u}\nAssistant:", "completion": f" {a}"}

def export_jsonl(out="ft_data.jsonl"):
    with open(out, "w", encoding="utf-8") as f:
        for item in build_pairs():
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print("Exported.")

if __name__=="__main__":
    export_jsonl()
