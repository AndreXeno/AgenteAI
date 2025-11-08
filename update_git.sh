#!/bin/bash
# ================================================
# 🚀 Script di aggiornamento Git automatico
# Progetto: AgenteAI
# Autore: Andrea Meneghetti
# ================================================

# Vai nella cartella del progetto
cd /Users/andreameneghetti/PycharmProjects/AgenteAI || exit

echo "=============================================="
echo "🔄 AGGIORNAMENTO GIT — AgenteAI"
echo "=============================================="

# Mostra lo stato attuale
git status

# Aggiungi tutte le modifiche
git add .

# Crea un commit con timestamp automatico
commit_msg="Auto-update: $(date '+%Y-%m-%d %H:%M:%S') —aggiustare collegamento strava(al momento non ce myfitnespal)"
git commit -m "$commit_msg"

# Allinea con il repository remoto
echo "📥 Pull da remoto..."
git pull origin main --rebase

# Spingi le modifiche su GitHub
echo "🚀 Push su remoto..."
git push origin main

# Mostra ultimi commit
echo "✅ Ultimi commit:"
git log --oneline -5

echo "=============================================="
echo "🎉 Aggiornamento completato con successo!"
echo "=============================================="