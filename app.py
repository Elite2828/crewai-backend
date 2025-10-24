from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import requests

app = Flask(__name__)

# 🧠 Function to communicate with your CrewAI backend
def run_crewai_agent(user_message):
    try:
        r = requests.post(
            "https://crewai-backend-slmc.onrender.com/api/chat",  # Your CrewAI backend endpoint
            json={"message": user_message},
            timeout=15
        )
        response = r.json().get("response", "Sorry, I didn’t understand that.")
    except Exception as e:
        print("CrewAI backend error:", e)
        response = "Sorry, I’m having trouble connecting to CrewAI right now."
    return response


# 🎙️ Voice endpoint for Twilio to call
@app.route("/voice", methods=['POST'])
def voice():
    # Capture speech or fallback to text
    user_input = request.form.get('SpeechResult') or "Hello, how can I help you?"
    
    # Send user’s voice text to your CrewAI backend
    ai_response = run_crewai_agent(user_input)
    
    # Create Twilio voice reply
    twiml = VoiceResponse()
    twiml.say(ai_response, voice='Polly.Joanna', language='en-US')
    
    return Response(str(twiml), mimetype="text/xml")


# ✅ Health check or manual test endpoint
@app.route("/")
def home():
    return "Voice AI Bot is running successfully!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
