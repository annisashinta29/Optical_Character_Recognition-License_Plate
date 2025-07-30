# Licence Plate OCR Evaluation using Character Error Rate (CER) on LMStudio and Python

Proyek ini bertujuan untuk melakukan evaluasi akurasi sistem OCR (Optical Character Recognition) terhadap gambar plat nomor kendaraan menggunakan pendekatan Character Error Rate (CER). Dataset berasal dari file gambar dan anotasi YOLO format per karakter. Sistem ini terdiri dari dua tahap utama:

1. Membuat file Ground Truth
Menggabungkan karakter hasil label YOLO menjadi string ground truth.
2. Memprediksi dan Evaluasi CER
Menggunakan model OCR berbasis Vision Language Model di LM Studio untuk memprediksi isi plat nomor, kemudian menghitung CER dengan formula:
<img width="231" height="86" alt="image" src="https://github.com/user-attachments/assets/b6cbf320-7a51-403d-a08d-5802840d25d5" />

dengan :
- S = jumlah karakter salah substitution
- D = jumlah karakter yang dihapus (deletion)
- I = jumlah karakter yang disispkan (insertion)
- N = panjang karakter pada ground truth

Hasil evaluasi ini nantinya akan disimpan dalam file .csv lengkap dengan nilai CER dan formula per kasus.

## 📁 Struktur Folder
<img width="436" height="223" alt="image" src="https://github.com/user-attachments/assets/57e91c28-ef93-420c-b4d7-213a73973e71" />

Keterangan :
1. Folder dataset berisi image dan label dengan format .txt dari setiap image
2. Code program untuk membuat file ground truth.csv (ground_truth.csv as output pertama)
3. Code program main untuk mengeksekusi project (saya memberi nama uas_computer_vison.py)
4. result.csv (output kedua setelah main program selesai dijalankan)

## 📋 Setup
### Instalasi LM Studio
- Install LM studio melalui : https://lmstudio.ai/download (install sesuai penggunaan : windows/linux/macOS)
  <img width="1006" height="775" alt="image" src="https://github.com/user-attachments/assets/4ae8949f-3a43-4da1-92d6-1f9b6f4419d9" />

- Masuk pada bagian Developer LMStudio
- Pastikan LM Studio (berjalan di localhost:1234)
<img width="1508" height="275" alt="image" src="https://github.com/user-attachments/assets/5db49552-320c-4ac8-ad05-cbe0189766fa" />

### Download Model Multimodal untuk mendukung VLM
- Model Vision Language seperti `ocrflux-3b`.
  
  Rekomendasi lain:
   -  `llava-v1.5-7b-gguf`
   -  `bakllava-1-gguf`
### Requiements
- Python 3.9
- Pandas
- Python-Levenshtein
- Library Python:
```bash
pip install requests pandas python-Levenshtein

```
## 📌 Eksekusi Code
### 1. generate_ground_truth.py
Jalankan pada terminal:
```bash
python generate_ground_truth.py
```
Script ini membaca semua file .txt hasil anotasi YOLO yang merepresentasikan karakter per baris dan menghasilkan file CSV ground_truth_new2.csv yang berisi:
- image: nama file gambar .jpg
- ground_truth: hasil gabungan karakter dari label (dengan spasi adaptif)

### 2. uas_computer_vision.py
jalankan :
```bash
python uas_computer_vision.py
```
Script ini akan:
- Membaca file ground_truth.csv
- Melakukan OCR ke masing-masing gambar menggunakan LM Studio
- Menghitung Character Error Rate (CER) menggunakan Levenshtein edit operations (S, D, I)
- Menyimpan hasil ke dalam results.csv dengan kolom:
  1. `image`
  2. `ground_truth`
  3. `prediction`
  4. `CER_score`
  5. `CER_formula (misalnya: CER = (2 + 0 + 1) / 8)`

## 📈 Output
(https://github.com/user-attachments/files/21515762/results.csv)
Setelah kedua program berhasil di eksekusi, maka tampilan pada file `result.csv`"
<img width="768" height="434" alt="image" src="https://github.com/user-attachments/assets/9a997e09-5250-4ff1-8568-b657b9817e56" />


## 🛠 Tips
Dalam mengeksekusi project ini:
1. Pastikan gambar dan file .txt ada di folder yang sama.
2. Ubah path folder di dalam script jika lokasi dataset berbeda.
3. LM Studio harus aktif dan mendukung input gambar base64.
4. Script ini dapat dengan mudah dimodifikasi untuk jenis OCR lainnya.

Link Youtube : https://youtu.be/I5N2cyHO8So 

 
  










