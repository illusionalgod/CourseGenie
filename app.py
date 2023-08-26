import os
import openai
from dotenv import load_dotenv
from flask import Flask, render_template, request
from chatbot_logic import get_response, get_moderation, INSTRUCTIONS

# load values from the .env file if it exists
load_dotenv()

# configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Flask app setup
app = Flask(__name__)

INSTRUCTIONS = INSTRUCTIONS

TEMPERATURE = 0.5
MAX_TOKENS = 200
FREQUENCY_PENALTY = 0
PRESENCE_PENALTY = 0.6
# limits how many questions we include in the prompt
MAX_CONTEXT_QUESTIONS = 5


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/agreement')
def agreement():
    return render_template('agreement.html')

@app.route('/chat', methods=['POST'])
def chat():
    new_question = request.form['question']
    errors = get_moderation(new_question)
    if errors:
        for error in errors:
            print(error)
        return redirect(url_for('chat'))

    response = get_response(INSTRUCTIONS, [], new_question)

    return response

@app.route('/start', methods=['POST'])
def start():
    return redirect(url_for('index'))

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
