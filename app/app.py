from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)
model = joblib.load('model_stunting.pkl')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    usia_bulan = data['usia_bulan']
    jenis_kelamin = 0 if data['jenis_kelamin'] == 'Laki-laki' else 1
    berat_kg = data['berat_kg']
    tinggi_cm = data['tinggi_cm']
    
    features = np.array([[usia_bulan, jenis_kelamin, berat_kg, tinggi_cm]])
    prediction = model.predict(features)
    
    hasil = 'Normal' if prediction[0] == 0 else 'Stunting'
    
    return jsonify({'hasil': hasil})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
