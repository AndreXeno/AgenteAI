from flask import Flask, render_template, request, jsonify
from agents.mindbody_agent import MindBodyAgent
import os

app = Flask(__name__)

# Initialize the agent
agent = MindBodyAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat')
def chat_page():
    return render_template('chat.html')

@app.route('/mental-wellbeing')
def mental_wellbeing_page():
    return render_template('mental_wellbeing.html')

@app.route('/psychologist/anika-sharma')
def psychologist_profile():
    return render_template('psychologist_profile.html')

@app.route('/psychologist/anika-sharma/contact')
def contact_psychologist():
    return render_template('contact_psychologist.html')

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
    app.run(debug=True, port=5000)
