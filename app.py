from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load model Random Forest
model = joblib.load('model_random_forest_stunting.pkl')  # Sesuaikan nama model kamu

# Fungsi rekomendasi kesehatan
def rekomendasi_kesehatan(prediksi, konsultasi):
    rekomendasi = []
    if prediksi == 1:  # Terindikasi Stunting
        rekomendasi.append("Anak terindikasi berisiko stunting. Segera konsultasikan ke posyandu atau dokter anak.")
        if konsultasi[0] == 1:
            rekomendasi.append("Ibu mengalami KEK saat hamil. Disarankan memperbaiki pola makan dengan kalori sehat dan protein tinggi.")
        if konsultasi[1] == 1:
            rekomendasi.append("Pola asuh kurang baik. Tingkatkan interaksi hangat dan stimulasi perkembangan anak.")
        if konsultasi[2] == 1:
            rekomendasi.append("Lingkungan rumah kurang bersih. Pastikan sanitasi dan air bersih tersedia.")
        if konsultasi[3] == 1:
            rekomendasi.append("Anak kekurangan gizi. Tingkatkan asupan protein hewani seperti telur, ikan, dan susu.")
        if konsultasi[4] == 1:
            rekomendasi.append("Kurangnya edukasi gizi ibu. Ikuti program edukasi posyandu atau konsultasi gizi anak.")
        if konsultasi[5] == 1:
            rekomendasi.append("Anemia saat hamil. Perbaiki konsumsi zat besi dan vitamin C.")
        rekomendasi.append("Lakukan kontrol pertumbuhan rutin ke posyandu setiap bulan.")
    else:  # Normal
        rekomendasi.append("Anak dalam pertumbuhan normal. Pertahankan pola asuh, asupan gizi, dan kontrol rutin ke posyandu.")
        if konsultasi[7] == 1:
            rekomendasi.append("Pola asuh baik. Teruskan stimulasi motorik dan kognitif anak.")
        if konsultasi[8] == 1:
            rekomendasi.append("Kebersihan rumah baik. Jaga sanitasi dan kebiasaan cuci tangan keluarga.")
        if konsultasi[9] == 1:
            rekomendasi.append("MP-ASI tepat waktu. Lanjutkan pemberian makanan seimbang dan bervariasi.")
        if konsultasi[10] == 1:
            rekomendasi.append("Gizi beragam tercapai. Pertahankan konsumsi dari semua kelompok makanan.")
        if konsultasi[11] == 1:
            rekomendasi.append("ASI Eksklusif sudah diberikan. Lanjutkan hingga usia 2 tahun sambil MP-ASI.")
    return rekomendasi

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        usia_bulan = data['usia_bulan']
        jenis_kelamin = data['jenis_kelamin']
        berat_badan = data['berat_badan']
        tinggi_badan = data['tinggi_badan']
        konsultasi = data['konsultasi']  # Harus array panjang 12
        
        # Encode jenis kelamin
        jk = 0 if jenis_kelamin == 'Laki-Laki' else 1

        # Buat array fitur model
        fitur_input = np.array([[usia_bulan, jk, berat_badan, tinggi_badan] + konsultasi])

        # Prediksi
        prediksi = model.predict(fitur_input)[0]

        # Generate rekomendasi
        rekomendasi = rekomendasi_kesehatan(prediksi, konsultasi)

        # Hasil
        hasil = 'Normal' if prediksi == 0 else 'Terindikasi Stunting'

        return jsonify({
            'prediksi': hasil,
            'rekomendasi': rekomendasi
        })

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
