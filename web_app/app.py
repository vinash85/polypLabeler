from flask import Flask, render_template, request, jsonify
import json
import csv
import os

app = Flask(__name__)

# Load questions
with open("questions.json", "r") as f:
    questions = json.load(f)

# Path to CSV file
csv_file = "responses.csv"

# Create CSV file with header if it doesn't exist
if not os.path.exists(csv_file):
    with open(csv_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["image", "question", "selected_answer"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_question/<int:index>")
def get_question(index):
    if 0 <= index < len(questions):
        return jsonify(questions[index])
    return jsonify({"error": "No more questions"}), 404

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    data = request.json
    # Find the question text using the image name
    question_text = next((q["question"] for q in questions if q["image"] == data["image"]), "Unknown")
    
    # Write to CSV
    with open(csv_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([data["image"], question_text, data["answer"]])
    
    print(f"Answer saved: {data}")
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=False,host="0.0.0.0")
