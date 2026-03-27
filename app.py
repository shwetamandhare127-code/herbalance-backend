from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import sqlite3
from flask_cors import CORS

# -------------------------------
# Database Connection
# -------------------------------
conn = sqlite3.connect('herbalance.db', check_same_thread=False)
cursor = conn.cursor()

app = Flask(__name__)
CORS(app)

# -------------------------------
# Load trained model
# -------------------------------
model = pickle.load(open("pcos_model.pkl", "rb"))

# -------------------------------
# Home Route
# -------------------------------
@app.route('/')
def home():
    return jsonify({
        "message": "PCOS Prediction API Running",
        "status": "success"
    })

# -------------------------------
# Prediction Route
# -------------------------------
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Validation
        if not data:
            return jsonify({
                "status": "error",
                "message": "No input data provided"
            }), 400

        required_fields = ['age', 'weight', 'bmi']
        for field in required_fields:
            if data.get(field) is None:
                return jsonify({
                    "status": "error",
                    "message": f"{field} is required"
                }), 400

        # -------------------------------
        # Features
        # -------------------------------
        features = [
            data.get('age', 0),
            data.get('weight', 0),
            data.get('bmi', 0),
            data.get('cycle_length', 0),
            data.get('hair_growth', 0),
            data.get('skin_darkening', 0),
            data.get('pimples', 0),
            data.get('weight_gain', 0),
            data.get('fast_food', 0),
            data.get('exercise', 0)
        ]

        final_features = pd.DataFrame([features])

        # -------------------------------
        # Prediction
        # -------------------------------
        prediction = model.predict(final_features)[0]

        try:
            probs = model.predict_proba(final_features)[0]
            confidence = round(max(probs) * 100, 2)
        except:
            confidence = 65.0

        confidence = min(max(confidence, 40.0), 95.0)

        # -------------------------------
        # Result
        # -------------------------------
        result = "PCOS Likely" if prediction == 1 else "PCOS Not Likely"

        # -------------------------------
        # Severity
        # -------------------------------
        if prediction == 1 and confidence > 75:
            severity = "High Risk"
        elif prediction == 1:
            severity = "Moderate Risk"
        else:
            severity = "Low Risk"

        # -------------------------------
        # Recommendations
        # -------------------------------
        advice = []

        if data.get('weight_gain') == 1:
            advice.append("Focus on weight management and balanced diet")

        if data.get('fast_food') == 1:
            advice.append("Avoid junk and processed food")

        if data.get('exercise') == 0:
            advice.append("Start regular physical activity")

        if data.get('hair_growth') == 1:
            advice.append("Consult doctor for hormonal imbalance")

        if data.get('pimples') == 1:
            advice.append("Maintain proper skincare and hydration")

        if data.get('cycle_length', 0) > 35:
            advice.append("Track menstrual cycle and consult a gynecologist")

        if len(advice) == 0:
            advice.append("Maintain a healthy lifestyle")

        # -------------------------------
        # Reasons
        # -------------------------------
        reasons = []

        if data.get('weight_gain') == 1:
            reasons.append("Weight gain observed")

        if data.get('cycle_length', 0) > 35:
            reasons.append("Irregular menstrual cycle")

        if data.get('hair_growth') == 1:
            reasons.append("Excess hair growth symptom")

        if data.get('pimples') == 1:
            reasons.append("Acne issues detected")

        # -------------------------------
        # Save to DB
        # -------------------------------
        try:
            cursor.execute('''
            INSERT INTO users (
                username, age, weight, bmi, cycle_length,
                hair_growth, skin_darkening, pimples,
                weight_gain, fast_food, exercise,
                prediction, confidence, severity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                data.get('username'),
                data.get('age'),
                data.get('weight'),
                data.get('bmi'),
                data.get('cycle_length'),
                data.get('hair_growth'),
                data.get('skin_darkening'),
                data.get('pimples'),
                data.get('weight_gain'),
                data.get('fast_food'),
                data.get('exercise'),
                result,
                confidence,
                severity
            ))

            conn.commit()
        except Exception as e:
            print("DB Error:", e)

        # -------------------------------
        # FINAL RESPONSE (FRONTEND READY)
        # -------------------------------
        return jsonify({
            "status": "success",
            "data": {
                "prediction": result,
                "confidence": confidence,
                "severity": severity,
                "risk_score": int(confidence),
                "reasons": reasons,
                "recommendations": advice
            }
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# -------------------------------
# History API
# -------------------------------
@app.route('/history', methods=['GET'])
def get_history():
    cursor.execute("""
        SELECT id, username, age, weight, bmi, cycle_length, prediction, confidence, severity 
        FROM users
    """)
    
    rows = cursor.fetchall()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "username": row[1],
            "age": row[2],
            "weight": row[3],
            "bmi": row[4],
            "cycle_length": row[5],
            "prediction": row[6],
            "confidence": row[7],
            "severity": row[8]
        })

    return jsonify({
        "status": "success",
        "data": result
    })


# -------------------------------
# Run App
# -------------------------------
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)