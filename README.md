# 🚲 Bike Sharing Data Analysis Dashboard
---

## 📊 Deskripsi Proyek

Tujuan utama proyek ini adalah untuk:
1. Menganalisis faktor-faktor yang memengaruhi jumlah penyewaan sepeda.
2. Mengetahui tren penyewaan berdasarkan waktu, musim, dan kondisi cuaca.
3. Membuat **dashboard interaktif** menggunakan Streamlit agar hasil analisis mudah dipahami.

Dataset terdiri dari dua bagian:
- `day.csv` → data penyewaan per hari.  
- `hour.csv` → data penyewaan per jam.  

Dalam proyek ini, fokus utama analisis dilakukan pada **data harian (`day_df`)** karena sudah merepresentasikan hasil agregasi dari `hour_df`.

---

## Setup Environment - Anaconda
```
conda create --name main-ds python=3.13
conda activate main-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
python -m venv venv
venv/Scripts/activate # Windows
source venv/bin/activate # Linux/Mac
pip install -r requirements.txt
```
or using `pipenv`
```
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run steamlit app
```
cd dashboard
streamlit run dashboard.py
```
