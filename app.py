from flask import Flask, render_template, request, jsonify
from utils import model_predict
from mails import getEmails
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/predict', methods=['POST'])
def predict():
    email = request.form.get('content')
    
    all_mails,preds= getEmails()
    return render_template("index.html", all_mails=all_mails,preds=preds)

# Create an API endpoint
# @app.route('/api/predict', methods=['POST'])
# def predict_api():
#     data = request.get_json(force=True)  # Get data posted as a json
#     email = data['content']
#     prediction = model_predict(email)
#     return jsonify({'prediction': prediction, 'email': email})  # Return prediction

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
