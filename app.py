from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from flask import Flask, render_template, request, jsonify
import model  # Importing the ML model logic

app = Flask(__name__)

# Load saved model, scaler, and label encoders
model = joblib.load('voting_classifier_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Define the selected features for testing
selected_features = ['incident_severity', 'vehicle_claim', 'total_claim_amount', 'property_claim', 'authorities_contacted', 'injury_claim']

print("Using these features for testing:", selected_features)

# Function to preprocess user input
def preprocess_input(user_input):
    input_df = pd.DataFrame([user_input])

    # Encode categorical features using the saved LabelEncoders
    for col in input_df.columns:
        if col in label_encoders:
            input_df[col] = label_encoders[col].transform([str(input_df[col].iloc[0])])  # Convert to string to handle '?'

    # Scale numerical features using the saved scaler
    input_scaled = scaler.transform(input_df)

    return input_scaled

# Route for the home page (input form)
@app.route('/input', methods=['GET'])
def home():
    return render_template('input.html', selected_features=selected_features, label_encoders=label_encoders)

# Route to handle form submission and display prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        user_input = {}
        for feature in selected_features:
            user_input[feature] = request.form[feature]

        # Preprocess the input
        input_processed = preprocess_input(user_input)

        # Make prediction
        prediction = model.predict(input_processed)
        prediction_proba = model.predict_proba(input_processed)[:, 1]

        # Prepare the result
        if prediction[0] == 1:
            result = "Fraudulent Policy"
            confidence = prediction_proba[0] * 100
        else:
            result = "Non-Fraudulent Policy"
            confidence = (1 - prediction_proba[0]) * 100

        # Render the output template with the result
        return render_template('output.html', recommendations=[{
            "recommendation": result,
            "confidence": f"{confidence:.2f}%"
        }])

    except Exception as e:
        # Handle errors gracefully
        return render_template('output.html', error=str(e))

from flask import Flask, render_template, request, redirect, url_for
import joblib
import pandas as pd

try:
    pipeline = joblib.load('model/upsell_ensemble_model.pkl')
except Exception as e:
    print(f"Error loading model: {e}")
    pipeline = None

# Generalized recommendations mapping
recommendations_mapping = {
    0: 'Cross-sell opportunity: Suggest savings or credit products with low fees',
    1: 'Engagement incentive: Personalized offers or loyalty points for early tenure engagement',
    2: 'General offer: Reward program or tailored financial review',
    3: 'Long-tenured customer: Recommend premium financial products or exclusive memberships',
    4: 'Mid-term tenure: Suggest insurance, fixed deposits, or personal loans with incentives',
    5: 'Premium policy offer: Investment or wealth management plans',
    6: 'Retention offer: Special cashback or reduced fees to retain the customer'
}

# Mapping of generalized features to specific policies
specific_policies_mapping = {
    0: ['SBI Life - Smart Bachat Plus', 'SBI Life - Smart Swadhan Supreme'],
    1: ['SBI Life - eShield Next', 'SBI Life - Saral Jeevan Bima'],
    2: ['SBI Life - Smart Platina Supreme', 'SBI Life - Smart Platina Plus'],
    3: ['SBI Life - Smart Elite Plus', 'SBI Life - Smart Fortune Builder'],
    4: ['SBI Life - Smart Scholar Plus', 'SBI Life - Retire Smart Plus'],
    5: ['SBI Life - eWealth Plus', 'SBI Life - Smart Annuity Plus'],
    6: ['SBI Life - Smart Platina Assure']
}

# Mapping policy names to their descriptions
policy_descriptions_mapping = {
    "SBI Life - Smart Bachat Plus": "A savings-oriented life insurance plan with guaranteed additions.",
    "SBI Life - Smart Swadhan Supreme": "A term insurance plan with return of premiums at policy end.",
    "SBI Life - eShield Next": "A pure risk premium life insurance plan with flexible coverage options.",
    "SBI Life - Saral Jeevan Bima": "A standard term plan with simple and affordable protection.",
    "SBI Life - Smart Platina Supreme": "A savings plan offering guaranteed regular income and life cover.",
    "SBI Life - Smart Platina Plus": "A life insurance savings plan with guaranteed returns.",
    "SBI Life - Smart Elite Plus": "A unit-linked insurance plan (ULIP) for high net-worth individuals.",
    "SBI Life - Smart Fortune Builder": "A unit-linked life insurance plan for wealth creation.",
    "SBI Life - Smart Scholar Plus": "A ULIP designed to secure your child’s future.",
    "SBI Life - Retire Smart Plus": "A unit-linked pension plan for retirement planning.",
    "SBI Life - eWealth Plus": "An online ULIP with automatic asset allocation.",
    "SBI Life - Smart Annuity Plus": "An immediate annuity plan ensuring a lifelong income.",
    "SBI Life - Smart Platina Assure": "A life insurance savings product with guaranteed returns."
}

@app.route('/upsell')
def index():
    return render_template('upsellinput.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract form data
        data = {
            'CreditScore': [int(request.form['CreditScore'])],
            'Geography': [request.form['Geography']],
            'Gender': [request.form['Gender']],
            'Age': [int(request.form['Age'])],
            'Tenure': [int(request.form['Tenure'])],
            'Balance': [float(request.form['Balance'])],
            'NumOfProducts': [int(request.form['NumOfProducts'])],
            'HasCrCard': [int(request.form['HasCrCard'])],
            'IsActiveMember': [int(request.form['IsActiveMember'])],
            'EstimatedSalary': [float(request.form['EstimatedSalary'])],
            'Exited': [int(request.form['Exited'])]
        }

        # Convert to DataFrame
        df = pd.DataFrame(data)

        # Check if model is loaded
        if pipeline is None:
            return render_template('upselloutput.html', recommendations=[], error='Model not loaded. Please check your model path.')

        # Make prediction and get probabilities
        probabilities = pipeline.predict_proba(df)[0]

        # Create a list of recommendation-confidence pairs
        recommendations_with_confidence = [
            {
                'recommendation': recommendations_mapping[i],
                'confidence': f"{probabilities[i] * 100:.2f}%",
                'id': i  # Add ID for redirection
            }
            for i in range(len(probabilities))
        ]

        # Sort recommendations by confidence (descending)
        recommendations_with_confidence.sort(key=lambda x: float(x['confidence'].strip('%')), reverse=True)

        return render_template('upselloutput.html', recommendations=recommendations_with_confidence)

    except Exception as e:
        print(f"Error during prediction: {e}")
        return render_template('upselloutput.html', recommendations=[], error=f"Error: {e}")

@app.route('/specific_policies/<int:policy_id>')
def specific_policies(policy_id):
    # Get the specific policies for the selected category
    policies = specific_policies_mapping.get(policy_id, [])
    
    # Fetch descriptions for each policy and add additional display properties
    policy_details = [
        {
            'name': policy,
            'description': policy_descriptions_mapping.get(policy, 'No description available')
        }
        for policy in policies
    ]

    return render_template('upsellpolicy.html', policies=policy_details, category_id=policy_id)


@app.route('/finance')
def home():
    return render_template('finindex.html')

@app.route('/roadmap', methods=['POST'])
def roadmap():
    savings = float(request.form['savings'])
    goal = float(request.form['goal'])
    duration = int(request.form['duration'])
    risk = request.form['risk']

    roadmap = model.generate_roadmap(savings, goal, duration, risk)  # Call ML function

    return jsonify(roadmap) 
@app.route("/categorize", methods=["POST"])
def categorize():
    try:
        amount = float(request.form["amount"])
        description = request.form["description"].strip().lower()
        
        # Get category prediction
        category = model.categorize_transaction(amount, description)
        
        return jsonify({"category": category})
    except Exception as e:
        return jsonify({"error": str(e)}), 400
