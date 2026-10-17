
from flask import Flask, request, jsonify
import joblib
import pandas as pd
import csv
import os
import time
from datetime import datetime

app = Flask(__name__)

# Menentukan lokasi folder dan file model
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR.parent / "model_harga_laptop.joblib"

# Memuat model yang sudah disimpan
model = joblib.load(MODEL_PATH)

# Urutan fitur sesuai data pelatihan
FITUR = [
    "Status",
    "Brand",
    "CPU",
    "RAM",
    "Storage",
    "Storage type",
    "GPU",
    "Screen",
    "Touch"
]


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "pesan": "API Prediksi Harga Laptop aktif"
    })


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()

        if not data or "data" not in data:
            return jsonify({
                "error": "Input harus berisi objek data"
            }), 400

        df_input = pd.DataFrame([data["data"]])

        # Memastikan semua fitur tersedia
        if not all(fitur in df_input.columns for fitur in FITUR):
            return jsonify({
                "error": "Input harus memiliki 9 fitur laptop yang diperlukan",
                "fitur_wajib": FITUR
            }), 400

        df_input = df_input[FITUR]

        # Melakukan prediksi dan menghitung waktu pemrosesan
        mulai = time.perf_counter()
        hasil = float(model.predict(df_input)[0])
        waktu_prediksi = round(
            (time.perf_counter() - mulai) * 1000, 2
        )

        # Menentukan lokasi folder monitoring
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        FOLDER_MONITORING = os.path.join(BASE_DIR, "..", "monitoring")

        os.makedirs(FOLDER_MONITORING, exist_ok=True)

        file_log = os.path.join(
            FOLDER_MONITORING, "monitoring_prediksi.csv"
        )

        file_baru = not os.path.exists(file_log)

        with open(
            file_log, "a", newline="", encoding="utf-8"
        ) as f:
            writer = csv.writer(f)

            if file_baru:
                writer.writerow([
                    "waktu",
                    "prediksi_harga",
                    "latensi_ms"
                ])

            writer.writerow([
                datetime.now().isoformat(timespec="seconds"),
                round(hasil, 2),
                waktu_prediksi
            ])

        # Mengirim hasil prediksi
        return jsonify({
            "prediksi_harga": round(hasil, 2),
            "latensi_ms": waktu_prediksi,
            "monitoring": "Hasil prediksi berhasil dicatat"
        })

    except (TypeError, ValueError) as e:
        return jsonify({
            "error": str(e)
        }), 400

    except Exception:
        app.logger.exception("Prediksi gagal")
        return jsonify({
            "error": "Terjadi kesalahan saat memproses prediksi"
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
