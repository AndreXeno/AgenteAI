import os, json

SESSION_FILE = "data/active_sessions.json"

def save_session(username: str):
    os.makedirs("data", exist_ok=True)
    with open(SESSION_FILE, "w") as f:
        json.dump({"username": username}, f)

def load_session():
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("username")
    return None