import pickle
from flask import Flask, request, render_template, jsonify

# Loading the model
try:
    model_pickle = open("classifier.pkl", 'rb')
    clf = pickle.load(model_pickle)
except Exception as e:
    print(f"Error loading model: {e}")
    clf = None  # Handle case if model loading fails

app = Flask(__name__)

@app.route("/", methods=['GET'])
def first():
    return "<h1>Welcome to Learning of CICD Pipeline with MB</h1>"

@app.route('/home')
def home():
    return "<h1>Welcome!!!</h2>"

@app.route('/home/<guest>')
def home_guest(guest):
    return render_template('home.html', name=guest)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            # Retrieve form data
            applicant_income = float(request.form.get('Applicant Income'))
            credit_history = float(request.form.get('Credit History'))
            gender = request.form.get('gender')
            loan_amount = float(request.form.get('Loan Amount'))
            marriage_status = request.form.get('marriage')

            # Encoding categorical data
            Gender = 0 if gender == "Male" else 1
            Married = 0 if marriage_status == "Unmarried" else 1

            # Making predictions
            if clf is not None:
                prediction = clf.predict(
                    [[Gender, Married, applicant_income, loan_amount, credit_history]]
                )[0]

                # Determine prediction result
                pred = 'Approved' if prediction == 1 else 'Rejected'
            else:
                pred = "Model not loaded properly."

        except Exception as e:
            pred = f"Error occurred: {e}"

        # Return result
        return render_template(
            'predict.html',
            applicant_income=applicant_income,
            credit_history=credit_history,
            gender=gender,
            loan_amount=loan_amount,
            marriage_status=marriage_status,
            prediction=pred
        )

    # For GET request, render the form
    return render_template('predict.html', prediction=None)

if __name__ == "__main__":
    app.run(debug=True)
