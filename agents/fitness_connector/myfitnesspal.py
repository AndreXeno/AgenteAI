import os, json

DATA_DIR = "data/users"

def is_myfitnesspal_connected(username: str):
    """Verifica se l'utente ha collegato MyFitnessPal"""
    user_dir = os.path.join(DATA_DIR, username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    return "myfitnesspal" in tokens and "username" in tokens["myfitnesspal"] and "password" in tokens["myfitnesspal"]

def disconnect_myfitnesspal(username: str):
    """Disconnette MyFitnessPal rimuovendo il token"""
    user_dir = os.path.join(DATA_DIR, username)
    token_path = os.path.join(user_dir, "tokens.json")
    if not os.path.exists(token_path):
        return False
    with open(token_path, "r") as f:
        tokens = json.load(f)
    if "myfitnesspal" in tokens:
        del tokens["myfitnesspal"]
        with open(token_path, "w") as f:
            json.dump(tokens, f, indent=2)
        print(f"[LOG] 🔌 MyFitnessPal disconnesso per {username}")
        return True
    return False