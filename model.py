def generate_roadmap(savings, goal, duration, risk):
    """
    Generates a financial roadmap based on user input.
    
    Parameters:
        savings (float): Current savings amount
        goal (float): Target savings goal
        duration (int): Duration in months
        risk (str): Risk profile ("Low", "Medium", "High")

    Returns:
        dict: Contains required monthly savings & investment recommendations
    """

    # Expected annual returns based on risk profile
    risk_returns = {
        "Low": 0.06,    # 6% per year (FDs, Bonds)
        "Medium": 0.10,  # 10% per year (Mutual Funds)
        "High": 0.15     # 15% per year (Stocks, Crypto)
    }
    
    # Convert annual return to monthly
    monthly_return = risk_returns[risk] / 12

    # Future Value Formula: FV = PV * (1 + r)^n + Pmt * [((1 + r)^n - 1) / r]
    # Rearranging to find Pmt (monthly savings required)
    required_monthly_savings = (goal - (savings * ((1 + monthly_return) ** duration))) / \
                               (((1 + monthly_return) ** duration - 1) / monthly_return)
    
    # If required savings is negative, no additional savings needed
    if required_monthly_savings < 0:
        required_monthly_savings = 0

    # If required savings is too high, suggest changes
    suggestion = None
    if required_monthly_savings > (0.5 * savings):  # Assuming saving 50% of savings is too high
        suggestion = "Increase duration or risk appetite to achieve your goal."

    # Investment recommendations based on risk profile
    investment_options = {
        "Low": ["Fixed Deposits", "Government Bonds", "PPF"],
        "Medium": ["Mutual Funds", "Index Funds", "Balanced Funds"],
        "High": ["Stocks", "Cryptocurrency", "Real Estate"]
    }

    return {
        "monthly_savings_required": round(required_monthly_savings, 2),
        "recommended_investments": investment_options[risk],
        "suggestion": suggestion
    }
    
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer

# Sample dataset (This would ideally come from user data)
data = {
    'amount': [500, 1500, 50, 3000, 200, 10000, 120, 2000, 30, 700],
    'description': ['groceries', 'rent', 'video game', 'travel', 'fast food',
                    'shopping', 'movie ticket', 'school fees', 'lottery', 'gym'],
    'category': ['Essentials', 'Essentials', 'Unnecessary', 'Moderates', 'Unnecessary',
                 'Moderates', 'Unnecessary', 'Essentials', 'Unnecessary', 'Moderates']
}

df = pd.DataFrame(data)

# Encode categorical features
le = LabelEncoder()
df['category_encoded'] = le.fit_transform(df['category'])

# One-hot encode the description field
column_transformer = ColumnTransformer(
    [('desc_encoder', OneHotEncoder(), ['description'])],
    remainder='passthrough'
)

# Transform data
X = column_transformer.fit_transform(df[['description', 'amount']])
y = df['category_encoded']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Save the trained model and encoders
joblib.dump((model, le, column_transformer), 'transaction_model.pkl')


def categorize_transaction(amount, description):
    """ Predicts transaction category based on amount and description """
    model, le, column_transformer = joblib.load('transaction_model.pkl')
    transformed_input = column_transformer.transform([[description, amount]])
    category_encoded = model.predict(transformed_input)[0]
    return le.inverse_transform([category_encoded])[0]
