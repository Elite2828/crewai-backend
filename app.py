import os
import africastalking
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# ---------------------------
# CONFIGURATION SECTION
# ---------------------------

# Africa's Talking credentials
username = "sandbox"  # Change to your live username when you go live
api_key = "RuNZoC6ih"
africastalking.initialize(username, api_key)
voice = africastalking.Voice

# CrewAI endpoint and API key
CREWAI_URL = "https://ai-voice-receptionist-system-v1-dd88a02c-f2-d6f98e2a.crewai.com"
CREWAI_API_KEY = "pat_jZgLocZp4mTz46_ra1AYU0C6y_q34xLombGOONy3JT8"

# ---------------------------
# MAIN VOICE ROUTE
# ---------------------------

@app.route("/voice", methods=["POST"])
def voice_handler():
    """Handles incoming voice calls from Africa's Talking."""
    try:
        is_active = request.values.get("isActive")
        session_id = request.values.get("sessionId")
        caller_number = request.values.get("callerNumber")

        # If call is active, capture speech or DTMF input
        if is_active == "1":
            user_msg = request.values.get("SpeechResult", "Hello")

            # Send message to CrewAI
            headers = {
                "Authorization": f"Bearer {CREWAI_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {"message": user_msg}

            print(f"📞 Incoming voice message: {user_msg}")

            try:
                response = requests.post(
                    f"{CREWAI_URL}/api/chat",
                    json=payload,
                    headers=headers,
                    timeout=20
                )
                response.raise_for_status()
                crew_reply = response.json().get("reply", "Sorry, I didn’t understand.")
            except Exception as e:
                print(f"⚠️ Error contacting CrewAI: {e}")
                crew_reply = "Sorry, there was a problem reaching my brain. Please try again later."

            # Speak back response to caller
            response_xml = f"""
                <Response>
                    <Say>{crew_reply}</Say>
                    <GetDigits timeout="15" numDigits="1" finishOnKey="#">
                        <Say>Press 1 to repeat, or hang up to end.</Say>
                    </GetDigits>
                </Response>
            """
            return response_xml, 200, {"Content-Type": "application/xml"}

        else:
            # Call has ended
            print(f"📴 Call ended from {caller_number} (Session: {session_id})")
            return "Call has ended", 200

    except Exception as e:
        print(f"🚨 Error in voice_handler: {e}")
        return "Server error", 500


@app.route("/", methods=["GET"])
def home():
    return "✅ CrewAI Voice Receptionist is running successfully."


# ---------------------------
# RUN APP LOCALLY OR ON RENDER
# ---------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
