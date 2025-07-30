import requests
import pandas as pd
import base64
import mimetypes
from Levenshtein import editops

# Konfigurasi LM Studio
LMSTUDIO_API_URL = "http://127.0.0.1:1234/v1/chat/completions"
MODEL_NAME = "ocrflux-3b"

# Fungsi hitung CER dengan formula
def calculate_cer_and_formula(ground_truth, prediction):
    """
    CER = (S + D + I) / N
    S = jumlah karakter salah substitution
    D = jumlah karakter yang dihapus (deletion)
    I = jumlah karakter yang disispkan (insertion)
    N = panjang karakter pada ground truth 
    """
    gt = ground_truth.strip()
    pred = prediction.strip()
    N = max(len(gt), 1)

    ops = editops(gt, pred)
    S = sum(1 for op in ops if op[0] == 'replace')
    D = sum(1 for op in ops if op[0] == 'delete')
    I = sum(1 for op in ops if op[0] == 'insert')

    cer = (S + D + I) / N
    formula = f"({S} + {D} + {I}) / {N}"
    return cer, formula

# Fungsi encode gambar ke base64 
def encode_image_to_base64(image_path):
    #Detect tipe mime (berupa jpg/png)
    mime_type, _ = mimetypes.guess_type(image_path)
    if mime_type is None:
        mime_type = "image/jpeg" # default kalau gagal deteksi
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"

# Fungsi kirim gambar ke LM Studio 
def ocr_with_lmstudio(image_path):
    # Ubah gambar ke base64 karena Qwen2VL Vision butuh ini
    base64_image = encode_image_to_base64(image_path)
    
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": { "url": base64_image }
                    },
                    {
                        "type": "text",
                        "text": "What is the license plate number shown in this image? Respond only with the plate number."
                    }
                ]
            }
        ]
    }

    try:
        response = requests.post(LMSTUDIO_API_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except Exception as e:
        #tampilkan pesan error jika gagal
        error_text = response.text if 'response' in locals() else ''
        print(f"Gagal OCR {image_path}: {e} | {error_text[:200]}")
        return ""

# main program
def main():
    df = pd.read_csv("ground_truth.csv", delimiter=";")
    results = []

    for idx, row in df.iterrows():
        image_path = row["image"]
        ground_truth = row["ground_truth"]

        print(f"[{idx+1}/{len(df)}] Proses OCR: {image_path}")

        # prediksi dari LM Studio
        prediction = ocr_with_lmstudio(image_path)
        
        # Hitung CER dan formula
        cer, formula = calculate_cer_and_formula(ground_truth, prediction)

        #simpan hasilnya
        results.append({
            "image": image_path,
            "ground_truth": ground_truth,
            "prediction": prediction,
            "CER_score": round(cer, 4), #pembulatan 4 angka
            "CER_formula": f"CER = {formula}"
        })

    # save ke csv
    result_df = pd.DataFrame(results)
    result_df.to_csv("results.csv", sep=";", index=False)

    # count rata-rata CER
    avg_cer = result_df["CER_score"].mean()
    print("\n(ok) Proses selesai!")
    print(f"Rata-rata CER: {avg_cer:.4f}")
    print("Hasil tersimpan di results.csv")

if __name__ == "__main__":
    main()