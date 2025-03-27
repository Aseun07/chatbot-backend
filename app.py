from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your Hugging Face model API
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-3B"
import os
HF_API_KEY = os.getenv("HF_API_KEY")  # Get API key from environment variable
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.json
    user_message = data.get("message", "")

    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {"inputs": user_message}

    response = requests.post(HF_API_URL, headers=headers, json=payload)
    
    try:
        bot_reply = response.json()
        # Handling different response structures
        if isinstance(bot_reply, list) and len(bot_reply) > 0 and "generated_text" in bot_reply[0]:
            reply_text = bot_reply[0]["generated_text"]
        elif "generated_text" in bot_reply:
            reply_text = bot_reply["generated_text"]
        else:
            reply_text = "Sorry, I didn't understand that."

    except Exception as e:
        reply_text = "Error processing response."

    return jsonify({"response": reply_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
