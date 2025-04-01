from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import openai

load_dotenv()

app = Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json['message']
        
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": """Ты дружелюбный и полезный ассистент. 
                 Инструкции:
                 1. Всегда отвечай на русском языке
                 2. Давай четкие и понятные ответы
                 3. Используй простые слова
                 4. Если нужно что-то объяснить, используй примеры
                 5. Будь вежливым и позитивным"""},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        return jsonify({
            'response': response.choices[0].message['content']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
