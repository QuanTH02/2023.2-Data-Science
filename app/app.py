from flask import Flask, render_template, request, jsonify
from predict import *

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def render_predict():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def process_prediction():
    data = request.json
    print(data['screens'])

    if data.get('openingWeek'):
        prediction_result = predict_opening_week(data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['openingWeek'], data['userVote'], data['ratings'], data['criticVote'], data['metaScore'], data['country'])
    else:
        prediction_result = predict_no_opening_week(data['month'], data['year'], data['mpaa'], data['budget'], data['runtime'], data['screens'], data['criticVote'], data['metaScore'], data['country'])
    
    return jsonify({'prediction': prediction_result})

if __name__ == '__main__':
    app.run(debug=True)
