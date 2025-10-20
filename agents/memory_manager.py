# ======================================
# 💾 MODULE: MEMORY MANAGER — Gestione memoria conversazionale
# ======================================

class MemoryManager:
    def __init__(self, max_memory=8):
        self.memory = []
        self.max_memory = max_memory

    def add_message(self, role: str, content: str):
        """Aggiunge un messaggio alla memoria."""
        self.memory.append({"role": role, "content": content})
        if len(self.memory) > self.max_memory:
            self.memory.pop(0)

    def get_context(self):
        """Restituisce il contesto testuale formattato."""
        return "\n".join(
            [f"{m['role']}: {m['content']}" for m in self.memory]
        )

    def clear(self):
        """Pulisce la memoria (es. quando l’utente scrive 'reset')."""
        self.memory = []