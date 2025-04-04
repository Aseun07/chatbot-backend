from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Hugging Face API Configuration
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
HF_API_KEY = os.getenv("HF_API_KEY")  # Ensure the API key is set

@app.route("/")
def home():
    return "Welcome to the chatbot API!"

@app.route("/chat", methods=["POST"])
def chat():
    # Ensure JSON data is received properly
    data = request.get_json()
    
    if not data or "message" not in data:
        return jsonify({"error": "Invalid request. 'message' field is required."}), 400

    user_message = data["message"]

    if not HF_API_KEY:
        return jsonify({"error": "API key is missing. Set HF_API_KEY in environment variables."}), 500

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_message}

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload)
        response_data = response.json()

        # Handling different response structures
        if isinstance(response_data, list) and response_data and "generated_text" in response_data[0]:
            reply_text = response_data[0]["generated_text"]
        elif isinstance(response_data, dict) and "generated_text" in response_data:
            reply_text = response_data["generated_text"]
        else:
            reply_text = "Sorry, I didn't understand that."

    except Exception as e:
        reply_text = f"Error processing response: {str(e)}"

    return jsonify({"response": reply_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
