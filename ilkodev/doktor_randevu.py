from datetime import datetime

class Hasta:
    def __init__(self, hasta_id, ad, tc, telefon):
        self.hasta_id = hasta_id
        self.ad = ad
        self.tc = tc
        self.telefon = telefon
        self.randevularim = []

    def randevu_al(self, randevu_bilgisi):
        self.randevularim.append(randevu_bilgisi)

class Doktor:
    def __init__(self, doktor_id, ad, uzmanlik):
        self.doktor_id = doktor_id
        self.ad = ad
        self.uzmanlik = uzmanlik
        self.uygun_saatler = {
            "09:00": True, "10:00": True, "11:00": True, 
            "13:00": True, "14:00": True, "15:00": True
        }

    def uygunluk_kontrol(self, saat):
        return self.uygun_saatler.get(saat, False)

class Randevu:
    def __init__(self, randevu_id, tarih, saat, doktor, hasta):
        self.randevu_id = randevu_id
        self.tarih = tarih
        self.saat = saat
        self.doktor = doktor
        self.hasta = hasta

    def randevu_olustur(self):
        if self.doktor.uygunluk_kontrol(self.saat):
            self.doktor.uygun_saatler[self.saat] = False # O saati kapat
            self.hasta.randevu_al(f"{self.tarih} - {self.saat} | Dr. {self.doktor.ad}")
            return True
        return False

    def randevu_iptal(self):
        self.doktor.uygun_saatler[self.saat] = True # O saati tekrar aç
        print(f" {self.saat} randevusu iptal edildi.")


if __name__ == "__main__":
    dr1 = Doktor(1, "Oğulcan Akın", "Kardiyoloji")
    dr2 = Doktor(2, "Yusuf Udum", "Göz Hastalıkları")
    doktorlar = {1: dr1, 2: dr2}

    mevcut_hasta = Hasta(101, "İbrahim Efe", "12345678901", "5423549363")
    
    randevu_listesi = [] 

    while True:
        print("\n--- ONLINE DOKTOR RANDEVU SİSTEMİ ---")
        print("1. Doktorları ve Uygun Saatleri Listele")
        print("2. Randevu Al")
        print("3. Randevularımı Görüntüle (Günlük Liste)")
        print("4. Çıkış")
        
        secim = input("İşlem seçiniz: ")

        if secim == "1":
            print("\n--- DOKTOR LİSTESİ VE UYGUNLUK ---")
            for id, dr in doktorlar.items():
                musait_saatler = [s for s, m in dr.uygun_saatler.items() if m]
                print(f"ID: {id} | Dr. {dr.ad} ({dr.uzmanlik})")
                print(f"   Uygun Saatler: {', '.join(musait_saatler)}")

        elif secim == "2":
            dr_id = int(input("Doktor ID girin: "))
            if dr_id in doktorlar:
                secilen_dr = doktorlar[dr_id]
                saat = input("Saat seçin (Örn: 09:00): ")
                
                yeni_randevu = Randevu(len(randevu_listesi)+1, "23.04.2026", saat, secilen_dr, mevcut_hasta)
                
                if yeni_randevu.randevu_olustur():
                    randevu_listesi.append(yeni_randevu)
                    print(f" Randevu başarıyla oluşturuldu: Dr. {secilen_dr.ad} - {saat}")
                else:
                    print(" Seçilen saat dolu veya geçersiz!")
            else:
                print(" Geçersiz Doktor ID!")

        elif secim == "3":
            print(f"\n--- {mevcut_hasta.ad} İÇİN GÜNLÜK RANDEVU LİSTESİ ---")
            if not mevcut_hasta.randevularim:
                print("Henüz bir randevunuz bulunmamaktadır.")
            else:
                for r in mevcut_hasta.randevularim:
                    print(f"- {r}")

        elif secim == "4":
            print("Sistemden çıkılıyor...")
            break