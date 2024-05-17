from flask import Flask, render_template, request, jsonify

app = Flask(__name__, template_folder="templates")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['GET'])
def render_predict():
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def process_prediction():
    # Xử lý dữ liệu được gửi từ phương thức POST
    data = request.json
    print(data)
    
    # Thực hiện dự đoán dựa trên dữ liệu và trả về kết quả
    prediction_result = "This is a prediction result"
    return jsonify({'prediction': data})

if __name__ == '__main__':
    app.run(debug=True)
