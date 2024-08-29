import os
from flask import Flask, request, render_template
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
server = Flask(__name__)

# Define system prompt
system_prompt = (
    """You are a friendly customer service chatbot for Vodafone/ziggo.
    I want you to find the answer on their website: [Vodafone](https://www.vodafoneziggo.nl/).
    Try to help the customer solve their problem online as much as possible.
    At first, greet the customer and ask how you can help.
    After that, greet the customer by name, then say hi and welcome to Vodafone/Ziggo.
    Try to help the customer solve their problem online as much as possible.
    Wish the customer a good day."""
)

# Function to send a prompt to GPT
def send_gpt(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if you have access
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        response_message = response['choices'][0]['message']['content']
        return response_message
    except Exception as e:
        return str(e)

# Define Flask route
@server.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        question = request.form['question']
        response = send_gpt(question)
        return render_template('chat.html', res=response)
    return render_template('chat.html')

# Run the Flask server
if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=5000)
