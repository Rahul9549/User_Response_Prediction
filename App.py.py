from flask import Flask, render_template, request
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

# Load the Trained Model
model_path = "RF_Model.pkl"
scaler_path = "Scaler.pkl"

try:
    with open(model_path, "rb") as f:
        model = pickle.load(f)
    with open(scaler_path, "rb") as f:
        scaler = pickle.load(f)
except FileNotFoundError:
    print("Error: Model or scaler file not found.")
    exit()


@app.route("/")
def home():
    return render_template("Index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get user Input from Form
        daily_time_spent = float(request.form["Daily Time Spent on Site"])
        age = int(request.form["Age"])
        area_income = float(request.form["Area Income"])
        daily_internet_usage = float(request.form["Daily Internet Usage"])
        male = int(request.form["Male"])

        # Preprocess User Input
        input_data = np.array([[daily_time_spent, age, area_income, daily_internet_usage, male]])
        input_data_scaled = scaler.transform(input_data)

        # Make Prediction
        prediction = model.predict(input_data_scaled)

        # Return Prediction
        return render_template("Result.html", prediction=prediction)
    except Exception as e:
        print("Prediction error:", e)
        return "An error occurred during prediction."


if __name__ == "__main__":
    app.run(debug=True)

