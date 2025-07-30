import os
import csv

# find direktori and output file
folder = r"C:\Users\acer\Documents\Semester 6\RE 604 Computer Vision\UAS\uas_cer\test\Dataset"
output_csv = os.path.join(folder, "ground_truth_new2.csv")

# Mapping class_id ke karakter
label_map = {
    0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9',
    10: 'A', 11: 'B', 12: 'C', 13: 'D', 14: 'E', 15: 'F', 16: 'G', 17: 'H', 18: 'I', 19: 'J',
    20: 'K', 21: 'L', 22: 'M', 23: 'N', 24: 'O', 25: 'P', 26: 'Q', 27: 'R', 28: 'S', 29: 'T',
    30: 'U', 31: 'V', 32: 'W', 33: 'X', 34: 'Y', 35: 'Z'
}

# Fungsi gabung karakter dengan spasi adaptif
def group_plate_number(boxes, factor=1.6):
    """
    boxes: list of (x_center, char), sudah diurutkan
    factor: multiplier untuk menentukan kapan kasih spasi
    """
    if not boxes:
        return ""
    
    # Hitung semua gap antar karakter
    gaps = [boxes[i][0] - boxes[i-1][0] for i in range(1, len(boxes))]
    
    if not gaps:  # hanya 1 karakter
        return boxes[0][1]
    
    # Ambil rata-rata gap antar karakter
    avg_gap = sum(gaps) / len(gaps)
    threshold = avg_gap * factor  # ambang dinamis

    result = boxes[0][1]
    for i in range(1, len(boxes)):
        gap = boxes[i][0] - boxes[i-1][0]
        # Kasih spasi kalau jarak jauh lebih besar dari rata-rata
        if gap > threshold:
            result += " "
        result += boxes[i][1]
    
    return result

data = []

# Loop semua file .txt 
for file in os.listdir(folder):
    if file.endswith(".txt"):
        txt_path = os.path.join(folder, file)
        jpg_name = file.replace(".txt", ".jpg")

        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        boxes = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                class_id = int(parts[0])
                x_center = float(parts[1])  # normalized x_center dari YOLO
                char = label_map.get(class_id, '?')
                boxes.append((x_center, char))

        # Urutkan dari kiri ke kanan
        boxes.sort(key=lambda x: x[0])

        # Gabungkan jadi plat nomor dengan spasi adaptif
        plate_number = group_plate_number(boxes)

        # Simpan hasil
        data.append([jpg_name, plate_number])

# Simpan ke CSV pakai ; supaya langsung rapi di Excel
with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(["image", "ground_truth"])
    writer.writerows(data)

print(f"ground_truth.csv berhasil dibuat di: {output_csv}")