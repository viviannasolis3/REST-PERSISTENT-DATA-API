
# REST Persistent Data API

## Reflection

For this assignment, I created a Flask RESTful API that stores fictional clinical records in both a SQLite database and a JSON Lines file. I began by setting up the Python environment and installing Flask, Flask-SQLAlchemy, and Pydantic. Next, I defined a ClinicalData database model and a Pydantic schema to validate incoming patient information. I added three new fields: blood pressure, heart rate, and temperature. Then I implemented a POST endpoint to create records and a GET endpoint to retrieve records from SQLite.

What surprised me was how two storage formats can serve different purposes. SQLite makes it convenient to query structured records, while JSON Lines provides a readable, append-only history. My code evolved from simply receiving JSON to validating values, saving data, and handling errors. I now better understand how HTTP endpoints, validation schemas, and persistent storage work together. I would like to learn more about keeping both storage systems consistent when one write succeeds but the other fails.

## Setup

```bash
python -m venv .venv
```

Activate the virtual environment (`.venv\\Scripts\\activate` on Windows, or `source .venv/bin/activate` on macOS/Linux), then:

```bash
pip install -r requirements.txt
python app.py
```

## Test with curl

```bash
curl.exe -X POST http://127.0.0.1:5000/clinical/ -H "Content-Type: application/json" -d '{"patient_name":"Alex Example","age":28,"diagnosis":"Routine checkup","blood_pressure":"120/80","heart_rate":72,"temperature":98.6}'
curl.exe http://127.0.0.1:5000/clinical/
```

The POST example above uses quoting suitable for PowerShell. In Windows Command Prompt, escape the JSON double quotes instead. Check `clinical_data.db` with a SQLite viewer and `data/clinical_data.jsonl` with a text editor.

**Use fictional data only.** This educational example is not HIPAA-compliant and does not guarantee atomic writes across SQLite and JSONL.
