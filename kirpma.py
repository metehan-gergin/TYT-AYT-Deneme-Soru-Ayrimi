import os
import fitz  # PDF okuyucu (PyMuPDF)
import cv2
import numpy as np
from ultralytics import YOLO
import glob

# --- AYARLAR ---
MODEL_YOLU = "best.pt"           
PDF_KLASORU = "PDF_GIRIS"        
ANA_CIKIS = "KESILEN_SORULAR"    
GUVEN_ORANI = 0.25               
# 

def kirpma_islemini_baslat():
    print(f"✂️  OTOMATİK KIRPMA SİSTEMİ BAŞLATILIYOR...\n")
    
    # 1. Model Kontrolü
    if not os.path.exists(MODEL_YOLU):
        print("❌ HATA: 'best.pt' dosyası bulunamadı!")
        return

    # 2. Klasör Kontrolü
    if not os.path.exists(PDF_KLASORU):
        os.makedirs(PDF_KLASORU)
        print(f"⚠️ '{PDF_KLASORU}' klasörü yoktu, oluşturuldu.")
        print(f"👉 Lütfen PDF dosyalarını '{PDF_KLASORU}' içine at ve tekrar çalıştır.")
        return

    # 3. PDF Listesi
    pdf_listesi = glob.glob(os.path.join(PDF_KLASORU, "*.pdf"))
    if not pdf_listesi:
        print(f"❌ '{PDF_KLASORU}' klasöründe hiç PDF yok!")
        return

    print(f"📂 Toplam {len(pdf_listesi)} adet PDF bulundu. İşlem başlıyor...\n")
    model = YOLO(MODEL_YOLU)

    # --- ANA DÖNGÜ ---
    for pdf_yolu in pdf_listesi:
        pdf_adi = os.path.basename(pdf_yolu).replace(".pdf", "")
        print(f"📘 Dosya: {pdf_adi}")
        
        # Her PDF için özel klasör oluştur
        hedef_klasor = os.path.join(ANA_CIKIS, pdf_adi)
        if not os.path.exists(hedef_klasor):
            os.makedirs(hedef_klasor)

        # PDF'i Aç ve Oku
        doc = fitz.open(pdf_yolu)
        toplam_sayfa = len(doc)
        toplam_kesilen = 0

        for i in range(toplam_sayfa):
            page = doc[i]
            # Kaliteli okuma için Zoom (2x)
            pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
            
            # Formata Çevir (Resme dönüştür)
            img_np = np.frombuffer(pix.samples, dtype=np.uint8)
            img = img_np.reshape(pix.h, pix.w, pix.n)
            
            # Renk Ayarı (RGB -> BGR)
            if pix.n >= 4:
                img = cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
            else:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

            # --- YAPAY ZEKA TESPİTİ ---
            results = model(img, conf=GUVEN_ORANI, verbose=False)
            
            sayfa_ici_sayac = 1
            for r in results:
                boxes = r.boxes
                if len(boxes) > 0:
                    # Soruları sıraya diz (Yukarıdan aşağıya)
                    sirali_indexler = sorted(range(len(boxes)), key=lambda k: boxes[k].xyxy[0][1])
                    
                    for idx in sirali_indexler:
                        x1, y1, x2, y2 = map(int, boxes[idx].xyxy[0])
                        
                        # KES
                        soru_resmi = img[y1:y2, x1:x2]
                        
                        # KAYDET (Örn: Matematik/Sayfa_1_Soru_1.jpg)
                        dosya_ismi = f"{hedef_klasor}/Sayfa_{i+1}_Soru_{sayfa_ici_sayac}.jpg"
                        cv2.imwrite(dosya_ismi, soru_resmi)
                        
                        sayfa_ici_sayac += 1
                        toplam_kesilen += 1
            
            print(f"   └── Sayfa {i+1} bitti. ({sayfa_ici_sayac-1} soru)")

        doc.close()
        print(f"✅ Tamamlandı. Toplam {toplam_kesilen} soru ayrıştırıldı.\n")

    print(f"🏁 BÜTÜN İŞLEMLER BİTTİ.")
    print(f"Sorularını '{ANA_CIKIS}' klasöründe bulabilirsin.")

if __name__ == "__main__":
    kirpma_islemini_baslat()