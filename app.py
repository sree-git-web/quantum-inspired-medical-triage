import sqlite3
import joblib
from flask import Flask, request, render_template

app = Flask(__name__)

# Load trained ML model
model = joblib.load("triage_model.pkl")

# Database setup
conn = sqlite3.connect('patients.db')
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    age INTEGER,
    severity INTEGER,
    heart_rate INTEGER,
    bp_systolic INTEGER,
    bp_diastolic INTEGER,
    oxygen INTEGER,
    consciousness TEXT,
    symptoms TEXT,
    priority TEXT
)
''')
conn.commit()
conn.close()


@app.route('/')
def home():
    return render_template('index.html')


# Convert text inputs to numbers (same encoding logic as training)
def encode_inputs(consciousness, symptoms):

    consciousness_map = {
        "alert": 0,
        "verbal": 1,
        "pain": 2,
        "unresponsive": 3
    }

    symptoms_map = {
        "fever": 0,
        "cough": 1,
        "headache": 2,
        "chest pain": 3,
        "fatigue": 4,
        "nausea": 5
    }

    consciousness_encoded = consciousness_map.get(consciousness.lower(), 0)
    symptoms_encoded = symptoms_map.get(symptoms.lower(), 0)

    return consciousness_encoded, symptoms_encoded


@app.route('/triage')
def triage():

    age = int(request.args.get('age'))
    severity = int(request.args.get('severity'))
    heart_rate = int(request.args.get('heart_rate'))
    bp_systolic = int(request.args.get('bp_systolic'))
    bp_diastolic = int(request.args.get('bp_diastolic'))
    oxygen = int(request.args.get('oxygen'))
    consciousness = request.args.get('consciousness')
    symptoms = request.args.get('symptoms')

    # Encode text fields
    consciousness_encoded, symptoms_encoded = encode_inputs(consciousness, symptoms)

    # Prepare input for ML model
    input_data = [[
        age,
        severity,
        heart_rate,
        bp_systolic,
        bp_diastolic,
        oxygen,
        consciousness_encoded,
        symptoms_encoded
    ]]

    # Predict priority
    prediction = model.predict(input_data)
    priority_num = int(prediction[0])

    # Convert number to label
    priority_dict = {
        1: "Priority 1 (Critical)",
        2: "Priority 2 (High)",
        3: "Priority 3 (Medium)",
        4: "Priority 4 (Low)"
    }

    priority_text = priority_dict.get(priority_num, "Unknown")

    # Save to database
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO patients (age, severity, heart_rate, bp_systolic, bp_diastolic, oxygen, consciousness, symptoms, priority)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (age, severity, heart_rate, bp_systolic, bp_diastolic, oxygen, consciousness, symptoms, priority_text))

    conn.commit()
    conn.close()

    return render_template(
        'result.html',
        age=age,
        severity=severity,
        heart_rate=heart_rate,
        bp_systolic=bp_systolic,
        bp_diastolic=bp_diastolic,
        oxygen=oxygen,
        consciousness=consciousness,
        symptoms=symptoms,
        priority=priority_text,
        priority_num=priority_num
    )


@app.route('/history')
def history():
    conn = sqlite3.connect('patients.db')
    c = conn.cursor()
    c.execute('SELECT * FROM patients ORDER BY id ASC')
    patients = c.fetchall()
    conn.close()
    return render_template('history.html', patients=patients)


if __name__ == '__main__':
    app.run(debug=True)
