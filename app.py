from flask import Flask, render_template, request, redirect, url_for, session
import csv, os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "change-this-in-production"

LOG_FILE = "simulation_events.csv"

if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "participant_id", "event", "ip_address"])

def log_event(participant_id, event):
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.utcnow().isoformat(),
            participant_id,
            event,
            request.remote_addr
        ])

@app.route("/")
def consent():
    return render_template("consent.html", step=1)

@app.route("/start", methods=["POST"])
def start():
    participant_id = f"P-{datetime.utcnow().strftime('%H%M%S')}"
    session["participant_id"] = participant_id
    session["score"] = 0
    log_event(participant_id, "consent_given")
    return redirect(url_for("simulation"))

@app.route("/simulation")
def simulation():
    if "participant_id" not in session:
        return redirect(url_for("consent"))
    return render_template("fake_login.html", step=2)

@app.route("/submit", methods=["POST"])
def submit():
    if "participant_id" not in session:
        return redirect(url_for("consent"))
    pid = session["participant_id"]
    # Do NOT read request.form["password"] — only log the event.
    log_event(pid, "credential_submission_simulated")
    return redirect(url_for("training"))

@app.route("/training")
def training():
    if "participant_id" not in session:
        return redirect(url_for("consent"))
    log_event(session["participant_id"], "training_viewed")
    return render_template("training.html", step=3)

@app.route("/quiz")
def quiz():
    if "participant_id" not in session:
        return redirect(url_for("consent"))
    return render_template("quiz.html", step=4)

@app.route("/quiz_submit", methods=["POST"])
def quiz_submit():
    if "participant_id" not in session:
        return redirect(url_for("consent"))
    # Three questions, each worth 1 point
    answers = {
        "q1": "b",   # hover over links
        "q2": "c",   # type the URL directly
        "q3": "a",   # report to IT
    }
    score = sum(1 for q, correct in answers.items()
                if request.form.get(q) == correct)
    session["score"] = score
    log_event(session["participant_id"], f"quiz_completed_score_{score}")
    return render_template("quiz_result.html", step=4,
                           score=score, total=len(answers))

@app.route("/report")
def report():
    events = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, newline="") as f:
            events = list(csv.DictReader(f))
    return render_template("report.html", events=events)

if __name__ == "__main__":
    app.run(debug=True)