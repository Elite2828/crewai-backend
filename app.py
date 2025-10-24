from flask import Flask, request, jsonify
from crewai import Crew, Agent, Task
import os

app = Flask(__name__)

# Example CrewAI agent setup (replace with your real agents later)
def run_crewai_agent(user_message):
    agent = Agent(name="Voice Assistant", role="AI Assistant", goal="Understand user queries and respond helpfully")
    task = Task(description=user_message, expected_output="Helpful response")
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    return result

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    response = run_crewai_agent(user_msg)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
