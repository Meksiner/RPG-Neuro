import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# Load model and tokenizer
model_path = "DevidCipher/RPG-Neuro"
finetuned_model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
tokenizer.pad_token = tokenizer.eos_token

# Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"
finetuned_model.to(device)
print(f"Device set to use {device}")

# Dictionary to store conversation histories {chat_id: [(question, answer), ...]}
chat_histories = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_chat', methods=['POST'])
def create_chat():
    try:
        chat_id = str(uuid.uuid4())  # Generate unique chat ID
        chat_histories[chat_id] = []  # Initialize empty history
        return jsonify({'chat_id': chat_id})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/list_chats', methods=['GET'])
def list_chats():
    try:
        # Return list of chat IDs and a preview (e.g., first question)
        chats = [
            {
                'chat_id': chat_id,
                'preview': chat_histories[chat_id][0][0] if chat_histories[chat_id] else "New Chat"
            }
            for chat_id in chat_histories
        ]
        return jsonify({'chats': chats})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/get_chat/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    try:
        if chat_id not in chat_histories:
            return jsonify({'error': 'Chat not found'}), 404
        return jsonify({'history': chat_histories[chat_id]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.json
        question = data['question']
        chat_id = data.get('chat_id')

        if not chat_id or chat_id not in chat_histories:
            return jsonify({'error': 'Invalid or missing chat_id'}), 400

        # Form prompt with history (last 5 Q-A pairs)
        prompt = ""
        for past_q, past_a in chat_histories[chat_id][-5:]:
            prompt += f"Question: {past_q}\nAnswer: {past_a}\n"
        prompt += f"Question: {question}\nAnswer:"

        # Tokenize with truncation
        inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=1024)
        inputs = {k: v.to(device) for k, v in inputs.items()}

        # Generate response
        outputs = finetuned_model.generate(
            **inputs,
            max_new_tokens=50,
            do_sample=True,
            top_p=0.9,
            temperature=0.7,
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id
        )

        # Decode result
        result = tokenizer.decode(outputs[0], skip_special_tokens=True)
        answer_start = result.rfind("Answer:") + len("Answer:")
        answer = result[answer_start:].strip()

        # Save to chat history
        chat_histories[chat_id].append((question, answer))

        return jsonify({'answer': answer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
