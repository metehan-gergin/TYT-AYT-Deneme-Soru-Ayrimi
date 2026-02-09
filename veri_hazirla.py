import os
from pdf2image import convert_from_path

# --- AYARLAR ---
# Bilgisayarındaki Poppler yolu 
POPPLER_BIN_YOLU = r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\poppler-25.12.0\Library\bin"

# PDF dosyasının adı 
PDF_DOSYASI = "YKSye-DOGRU-2024-TYT.pdf"

# Resimlerin çıkacağı klasör
CIKTI_KLASORU = "Egitim_Verisi_Resimler5"
# --------------

def pdf_resme_cevir():
    print("İşlem başlıyor...")

    # 1. Klasör yoksa oluştur
    if not os.path.exists(CIKTI_KLASORU):
        os.makedirs(CIKTI_KLASORU)
        print(f"'{CIKTI_KLASORU}' klasörü oluşturuldu.")

    print(f"'{PDF_DOSYASI}' okunuyor ve resme çevriliyor. Lütfen bekle...")
    
    try:
        # 2. PDF'i resimlere çevir
        # dpi=200 yeterli, çok yüksek yaparsak bilgisayar kasabilir.
        images = convert_from_path(PDF_DOSYASI, dpi=200, poppler_path=POPPLER_BIN_YOLU)
        
        # 3. Resimleri kaydet
        toplam_sayfa = len(images)
        print(f"Toplam {toplam_sayfa} sayfa bulundu. Kaydediliyor...")

        for i, img in enumerate(images):
            # Dosya adı: Sayfa_1.jpg, Sayfa_2.jpg...
            dosya_adi = f"{CIKTI_KLASORU}/Sayfa_{i+1}.jpg"
            img.save(dosya_adi, "JPEG")
            
            # Her sayfada bilgi ver
            print(f" -> Sayfa {i+1} kaydedildi.")
            
        print("\nBİTTİ! Tüm sayfalar resme çevrildi.")
        print(f"Lütfen '{CIKTI_KLASORU}' klasörünü kontrol et.")

    except Exception as e:
        print("\n--- HATA OLUŞTU ---")
        print(f"Hata detayı: {e}")
        print("Lütfen PDF dosyasının adının doğru olduğundan ve kodla yan yana olduğundan emin ol.")

if __name__ == "__main__":
    pdf_resme_cevir()