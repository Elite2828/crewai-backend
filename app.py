from flask import Flask, request, jsonify
import africastalking
import os
import requests

app = Flask(__name__)

# Initialize Africa's Talking
username = "sandbox"  # or your live username when you go live
api_key = "RuNZoC6ih"
africastalking.initialize(username, api_key)

voice = africastalking.Voice

@app.route("/voice", methods=["POST"])
def voice_handler():
    # Africa's Talking sends 'isActive' when a call is ongoing
    is_active = request.values.get("isActive")

    if is_active == '1':
        caller_number = request.values.get("callerNumber")
        print("Incoming call from:", caller_number)

        # Send the speech/text to CrewAI backend
        try:
            user_message = "Incoming voice call from " + caller_number
            r = requests.post(
                "https://crewai-backend-slmc.onrender.com/api/chat",
                json={"message": user_message},
                timeout=15
            )
            response = r.json().get("response", "Sorry, I didn’t understand that.")
        except Exception as e:
            print("CrewAI backend error:", e)
            response = "Sorry, I’m having trouble connecting to CrewAI right now."

        # Return Africa's Talking Voice XML
        xml_response = f"""
        <Response>
            <Say>{response}</Say>
            <Hangup/>
        </Response>
        """
        return xml_response, 200, {"Content-Type": "application/xml"}

    else:
        # When the call ends
        print("Call ended.")
        return "OK", 200


@app.route("/", methods=["GET"])
def home():
    return "✅ CrewAI + Africa's Talking Voice Agent is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
    
