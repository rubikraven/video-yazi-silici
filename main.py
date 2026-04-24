import cv2
import numpy as np
import os

# --- AYARLAR ---
GIRIS_DOSYASI = "vecna-yazi-sil.mp4"
CIKIS_DOSYASI = "vecna-yazi-sil-kesin-sonuc.mp4"

# yeni ölçümler
X_YUZDE = 2.50
Y_YUZDE = 2.05

# Yazıyı tamamen yutması için genişlik ve yükseklik payı
W_YUZDE = 22.0  # Alanı sağa doğru
H_YUZDE = 6.5  # Yükseklik


# ---------------------------

def son_vurus_temizle():
    if not os.path.exists(GIRIS_DOSYASI):
        print(f"HATA: '{GIRIS_DOSYASI}' dosyası bulunamadı. Lütfen klasörü kontrol et.")
        return

    cap = cv2.VideoCapture(GIRIS_DOSYASI)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(CIKIS_DOSYASI, fourcc, fps, (width, height))

    # Milimetrik piksel hesaplama (Hafif sola/yukarı kaydırarak metni tam hapsediyoruz)
    x = int(width * ((X_YUZDE - 0.6) / 100))  # 0.2 puan sola kaydırıldı
    y = int(height * ((Y_YUZDE - 0.6) / 100))  # 0.2 puan yukarı kaydırıldı
    w = int(width * (W_YUZDE / 100))
    h = int(height * (H_YUZDE / 100))

    print(f"Temizleme modu: Aktif. {width}x{height} çözünürlükte temizlik yapılıyor...")

    count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 1. Maske: Yazının olduğu bölgeyi tamamen beyaza boya
        mask = np.zeros(frame.shape[:2], dtype=np.uint8)
        mask[y:y + h, x:x + w] = 255

        # 2. Inpaint: Çevredeki piksellerle o boşluğu doğal şekilde doldur
        # Radius değerini 5 yaparak daha güçlü bir 'leke giderici' etkisi sağlıyoruz
        cleaned_frame = cv2.inpaint(frame, mask, 5, cv2.INPAINT_TELEA)

        out.write(cleaned_frame)

        count += 1
        if count % 100 == 0:
            print(f"İlerleme: %{int((count / total) * 100)}")

    cap.release()
    out.release()
    print("\n" + "=" * 40)
    print(f"İŞLEM BAŞARIYLA TAMAMLANDI!")
    print(f"Dosya: {CIKIS_DOSYASI}")
    print("=" * 40)


if __name__ == "__main__":
    son_vurus_temizle()
