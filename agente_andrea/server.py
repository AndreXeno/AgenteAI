from flask import Flask, render_template, request, jsonify
from agents.mindbody_agent import MindBodyAgent
from agents.data_manager import log_mind_state
import os

app = Flask(__name__)

# Initialize the agent
agent = MindBodyAgent()

@app.route('/')
def home():
    return "Backend API Running. Use the frontend on port 5183."

@app.route('/api/mental-log', methods=['POST'])
def save_mental_log():
    data = request.json
    username = data.get('username', 'guest')
    mood = data.get('mood')
    emotions = data.get('emotions', [])
    note = data.get('note', '')
    
    success = log_mind_state(username, mood, emotions, note)
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error'}), 500

@app.route('/api/ai/analyze-mental-log', methods=['POST'])
def analyze_mental_log():
    data = request.json
    username = data.get('username', 'guest')
    
    insight = agent.analyze_mental_logs(username)
    return jsonify({'insight': insight})

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json
    user_input = data.get('message', '')
    username = data.get('username', 'guest')
    
    if not user_input:
        return jsonify({'response': 'Per favore, scrivi qualcosa.'})
    
    try:
        response = agent.run(user_input, username=username)
        response_text = response.text if hasattr(response, 'text') else str(response)
        return jsonify({'response': response_text})
    except Exception as e:
        print(f"Error processing message: {e}")
        return jsonify({'response': 'Mi dispiace, si è verificato un errore.'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
