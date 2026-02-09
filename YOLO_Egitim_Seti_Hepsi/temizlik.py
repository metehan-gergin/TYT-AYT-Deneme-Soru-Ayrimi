import os
import shutil

# --- AYARLAR ---
KAYNAK_KLASOR = "."       # Şu anki klasör
HEDEF_KLASOR = "TEMIZ_SET" # Oluşacak yeni klasör
# ----------------

def temizle_ve_duzelt():
    print("🧹 TEMİZLİK ROBOTU ÇALIŞIYOR (WİNDOWS MODU)...")
    
    if not os.path.exists(HEDEF_KLASOR):
        os.makedirs(HEDEF_KLASOR)

    # Klasördeki txt dosyalarını bul
    txt_dosyalari = [f for f in os.listdir(KAYNAK_KLASOR) if f.endswith(".txt") and f != "classes.txt"]
    
    if len(txt_dosyalari) == 0:
        print("❌ HATA: Hiç .txt dosyası bulunamadı! Bu scripti resimlerin olduğu yere attığına emin misin?")
        return

    tasinan_sayisi = 0
    
    for txt_ad in txt_dosyalari:
        # 1. Txt dosyasını oku ve '15'leri '0' yap
        try:
            with open(txt_ad, "r", encoding="utf-8") as f:
                lines = f.readlines()
            
            yeni_satirlar = []
            dosya_dolu = False
            for line in lines:
                parts = line.strip().split()
                if len(parts) > 0:
                    parts[0] = "0"  # SINIF NUMARASINI ZORLA 0 YAP
                    yeni_satirlar.append(" ".join(parts) + "\n")
                    dosya_dolu = True
            
            if not dosya_dolu:
                continue # Boş dosyayı geç

            # 2. Resim dosyasını bul (jpg veya png)
            resim_ad_jpg = txt_ad.replace(".txt", ".jpg")
            resim_ad_png = txt_ad.replace(".txt", ".png")
            
            bulunan_resim = ""
            if os.path.exists(resim_ad_jpg):
                bulunan_resim = resim_ad_jpg
            elif os.path.exists(resim_ad_png):
                bulunan_resim = resim_ad_png
                
            # 3. Eğer resmi varsa, ikisini de TEMIZ_SET klasörüne taşı
            if bulunan_resim:
                # Yeni txt'yi yaz
                with open(os.path.join(HEDEF_KLASOR, txt_ad), "w", encoding="utf-8") as f:
                    f.writelines(yeni_satirlar)
                
                # Resmi kopyala
                shutil.copy(bulunan_resim, os.path.join(HEDEF_KLASOR, bulunan_resim))
                tasinan_sayisi += 1
                print(f"✅ Kurtarıldı: {bulunan_resim}")
        except Exception as e:
            print(f"⚠️ Hata oluştu ({txt_ad}): {e}")
            
    print(f"\n🎉 BİTTİ! Toplam {tasinan_sayisi} adet veri 'TEMIZ_SET' klasörüne alındı.")
    print("Lütfen 'TEMIZ_SET' klasörünü kontrol et, sonra zip yap.")

if __name__ == "__main__":
    temizle_ve_duzelt()