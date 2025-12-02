# ======================================
# 💾 MODULE: MEMORY MANAGER — Gestione memoria conversazionale persistente
# ======================================

import os
import json
from datetime import datetime

DATA_DIR = "data/users"


class MemoryManager:
    def __init__(self, username: str = "anonimo", max_memory: int = 8):
        self.username = username
        self.max_memory = max_memory
        self.memory = []
        self.user_dir = os.path.join(DATA_DIR, username)
        os.makedirs(self.user_dir, exist_ok=True)
        self.file_path = os.path.join(self.user_dir, "memory.json")
        self.load()

    # ======================================
    # 🧠 FUNZIONI PRINCIPALI
    # ======================================
    def add_message(self, role: str, content: str):
        """Aggiunge un messaggio alla memoria e la salva in modo persistente."""
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        }
        self.memory.append(entry)
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)
        self.save()
        print(f"[LOG] 💾 Messaggio aggiunto ({role}): {content[:60]}...")

    def get_context(self) -> str:
        """Restituisce il contesto conversazionale formattato."""
        return "\n".join([f"{m['role'].capitalize()}: {m['content']}" for m in self.memory])

    def clear(self):
        """Pulisce la memoria e sovrascrive il file JSON."""
        self.memory = []
        self.save()
        print("[LOG] 🧹 Memoria cancellata.")

    # ======================================
    # 📦 PERSISTENZA SU FILE
    # ======================================
    def save(self):
        """Salva la memoria attuale su file JSON."""
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[ERROR] ❌ Errore nel salvataggio memoria: {e}")

    def load(self):
        """Carica la memoria dal file, se disponibile."""
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, "r", encoding="utf-8") as f:
                    self.memory = json.load(f)
                    print(f"[LOG] 🔄 Memoria caricata da {self.file_path} ({len(self.memory)} messaggi).")
            else:
                self.memory = []
        except Exception as e:
            print(f"[WARN] ⚠️ Errore nel caricamento della memoria: {e}")
            self.memory = []