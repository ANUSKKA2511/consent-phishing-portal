# Consent-Based Phishing Awareness Simulation & Training Portal

An ethical hacking coursework project that simulates a phishing login page
**only after informed consent**, never stores real credentials, and
immediately redirects participants to training material.

## Features
- Consent gate before any simulation
- Anonymised participant IDs (e.g. `P-101502`)
- Fake login page with visual red-flag reveal
- Interactive 3-question awareness quiz
- CSV event log that **never contains passwords or emails**

## Ethical Safeguards
- `/submit` route ignores `request.form["password"]`
- Only the *event* "credential_submission_simulated" is logged
- Participants can stop at any time

## Run Locally
```bash
pip install -r requirements.txt
python app.py