# Praktikum Machine Learning — Prediksi Harga Laptop

Project praktikum Machine Learning untuk memprediksi harga laptop berdasarkan spesifikasi menggunakan **Random Forest Regressor**. Project mencakup eksplorasi dan pembersihan data, preprocessing, pembagian data latih/uji, pelatihan dan evaluasi model, serta contoh deployment API dan pencatatan monitoring prediksi.

## Tujuan

- Memahami tahapan dasar pengolahan data untuk Machine Learning.
- Menganalisis hubungan spesifikasi laptop dengan harga.
- Membangun model regresi untuk memperkirakan harga laptop.
- Menyediakan endpoint API sederhana untuk menerima input spesifikasi dan mengembalikan hasil prediksi.
- Mencatat waktu prediksi dan hasilnya sebagai monitoring dasar.

## Teknologi yang Digunakan

- Python
- Jupyter Notebook
- Pandas dan NumPy
- Matplotlib dan Seaborn
- Scikit-learn
- Flask
- Joblib

## Struktur Project

```
praktikum-machine-learning/
├── Praktikum_Machine_Learning.ipynb  # Analisis data, preprocessing, training, evaluasi
├── laptops.csv                       # Dataset laptop
├── model_harga_laptop.joblib         # Model pipeline yang sudah dilatih
├── deployment/
│   ├── data.json                     # Contoh input untuk API
│   └── testing_deploy.py             # API prediksi berbasis Flask
└── monitoring/
    └── monitoring_prediksi.csv       # Log waktu, hasil prediksi, dan latensi
```

## Alur Pengerjaan

1. **Data Loading** — membaca dataset `laptops.csv` ke DataFrame.
2. **Data Cleaning** — memeriksa nilai kosong dan data duplikat, serta mengisi nilai kosong pada kolom `Storage type` dan `GPU` dengan `Unknown`.
3. **EDA (Exploratory Data Analysis)** — melihat ringkasan statistik dan membuat visualisasi distribusi harga, hubungan RAM dengan harga, serta harga berdasarkan merek.
4. **Data Processing** — menggunakan fitur spesifikasi laptop sebagai input dan `Final Price` sebagai target. Kolom `Laptop` dan `Model` tidak digunakan sebagai fitur model.
5. **Preprocessing** — nilai numerik yang kosong ditangani dengan median; fitur kategorikal ditangani dengan nilai yang paling sering muncul dan dikonversi menggunakan One-Hot Encoding.
6. **Data Splitting** — membagi data menjadi 80% data latih dan 20% data uji dengan `random_state=42`.
7. **Modelling** — melatih `RandomForestRegressor` dengan 200 estimator.
8. **Evaluation** — mengevaluasi model menggunakan MAE, RMSE, dan R² serta membandingkan harga aktual dengan harga prediksi.
9. **Deployment dan Monitoring** — menyediakan endpoint Flask `/predict` dan mencatat hasil prediksi serta latensi ke CSV.

## Hasil Evaluasi Model

Berdasarkan hasil praktikum yang tercatat:

| Metrik   |    Nilai |
| -------- | -------: |
| MAE      | 261.5955 |
| RMSE     | 445.7003 |
| R² Score |   0.7846 |

MAE menunjukkan rata-rata selisih absolut antara harga aktual dan prediksi. RMSE memberi penalti lebih besar pada kesalahan yang besar. R² sekitar 0,7846 menunjukkan model menjelaskan sekitar 78,46% variasi target pada data uji yang digunakan. Hasil dapat berbeda jika dataset atau konfigurasi model berubah.

## Menjalankan Notebook

1. Pastikan Python telah terpasang.
2. Instal library yang digunakan:

   ```bash
   pip install pandas numpy matplotlib seaborn scikit-learn jupyter
   ```

3. Buka `Praktikum_Machine_Learning.ipynb` di Jupyter Notebook atau VS Code.
4. Pastikan file `laptops.csv` berada di folder yang sama dengan notebook.
5. Jalankan sel notebook secara berurutan.

## Menjalankan API Prediksi

Instal dependensi API:

```bash
pip install flask joblib pandas scikit-learn numpy
```

Jalankan perintah berikut dari folder `deployment`:

```bash
python testing_deploy.py
```

API berjalan secara lokal menggunakan Flask. Endpoint yang tersedia:

- `GET /` — memeriksa apakah API aktif.
- `POST /predict` — mengirim spesifikasi laptop dan menerima prediksi harga.

### Contoh Input

File contoh tersedia di `deployment/data.json`:

```json
{
  "data": {
    "Status": "New",
    "Brand": "Acer",
    "CPU": "Intel Core i5",
    "RAM": 16,
    "Storage": 512,
    "Storage type": "SSD",
    "GPU": "Unknown",
    "Screen": 15.6,
    "Touch": "No"
  }
}
```

Kirim isi JSON tersebut sebagai body pada request `POST` ke `http://127.0.0.1:5000/predict` dengan header `Content-Type: application/json`. Respons mencakup `prediksi_harga`, `latensi_ms`, dan status pencatatan monitoring.

> Catatan: server pada script menggunakan `debug=True` untuk pengujian lokal. Jangan gunakan konfigurasi debug ini untuk deployment produksi.

## Monitoring

Setiap prediksi yang berhasil akan ditambahkan ke `monitoring/monitoring_prediksi.csv` dengan kolom:

- `waktu` — waktu prediksi dicatat.
- `prediksi_harga` — nilai prediksi model.
- `latensi_ms` — waktu proses prediksi dalam milidetik.

Log yang tersedia merupakan contoh pemantauan dasar. Log ini belum mengukur akurasi prediksi terhadap harga aktual karena harga aktual tidak dicatat pada endpoint tersebut.

## Dataset dan Atribusi

Dataset: **Laptops Price Dataset** oleh `juanmerinobermejo`.

Sumber: https://www.kaggle.com/datasets/juanmerinobermejo/laptops-price-dataset

Pada halaman Kaggle, dataset ditampilkan dengan lisensi **Apache 2.0**. Sebelum mendistribusikan salinan dataset, periksa kembali ketentuan lisensi pada halaman sumber dan pertahankan pemberitahuan hak cipta atau atribusi yang disediakan oleh pemilik dataset.

## Batasan

- Model merupakan hasil praktikum dan bukan penentu harga resmi.
- Akurasi prediksi bergantung pada kualitas dan cakupan dataset.
- API ini merupakan contoh deployment lokal sederhana, belum dilengkapi autentikasi, pembatasan request, atau konfigurasi produksi.
- File monitoring saat ini mencatat prediksi dan latensi, bukan evaluasi akurasi secara otomatis.

## Pengembangan Berikutnya

- Menambahkan validasi tipe dan rentang input API.
- Menambahkan pengujian otomatis untuk endpoint prediksi.
- Memantau perubahan distribusi input dan performa model dari waktu ke waktu.
- Menyiapkan deployment produksi dengan konfigurasi keamanan yang sesuai.
