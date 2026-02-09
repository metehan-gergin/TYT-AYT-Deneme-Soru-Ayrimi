import os
import shutil

# --- AYARLAR ---
# Buraya resimlerinin olduğu klasörlerin yollarını yaz 
# Örnek:
KLASORLER = [
    r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\TYT-AYT Deneme Soru Ayrımı - Geliştirmece\Egitim_Verisi_Resimler1",
    r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\TYT-AYT Deneme Soru Ayrımı - Geliştirmece\Egitim_Verisi_Resimler2",
    r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\TYT-AYT Deneme Soru Ayrımı - Geliştirmece\Egitim_Verisi_Resimler3",
    r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\TYT-AYT Deneme Soru Ayrımı - Geliştirmece\Egitim_Verisi_Resimler4",
    r"C:\Users\Metehandrov\OneDrive\1240810111111-Masaüstü\Masaüstü\TYT-AYT Deneme Soru Ayrımı - Geliştirmece\Egitim_Verisi_Resimler5",
]

# Hepsini toplayacağımız YENİ klasörün adı
HEDEF_KLASOR = r"C:\Users\Metehandrov\Desktop\YOLO_Egitim_Seti_Hepsi"
# --------------

def birlestir():
    if not os.path.exists(HEDEF_KLASOR):
        os.makedirs(HEDEF_KLASOR)
        print(f"'{HEDEF_KLASOR}' oluşturuldu.")

    toplam_sayac = 0

    for kaynak_klasor in KLASORLER:
        # Klasör adını al (örn: 'Egitim_Verisi_Resimler_2016')
        klasor_ismi = os.path.basename(kaynak_klasor)
        
        print(f"'{klasor_ismi}' içindeki dosyalar taşınıyor...")
        
        try:
            dosyalar = os.listdir(kaynak_klasor)
            for dosya in dosyalar:
                if dosya.lower().endswith(('.jpg', '.jpeg', '.png')):
                    # Eski dosya yolu
                    eski_yol = os.path.join(kaynak_klasor, dosya)
                    
                    # Yeni isim: KlasörAdı_EskiAd.jpg (Çakışmayı önler)
                    # Örn: 2016_Sayfa_1.jpg
                    yeni_isim = f"{klasor_ismi}_{dosya}"
                    yeni_yol = os.path.join(HEDEF_KLASOR, yeni_isim)
                    
                    shutil.copy2(eski_yol, yeni_yol)
                    toplam_sayac += 1
                    
        except Exception as e:
            print(f"Hata: {kaynak_klasor} bulunamadı veya okunamadı. ({e})")

    print(f"\nBİTTİ! Toplam {toplam_sayac} resim '{HEDEF_KLASOR}' içine toplandı.")
    print("LabelImg programında artık SADECE BU KLASÖRÜ açmalısın.")

if __name__ == "__main__":
    birlestir()