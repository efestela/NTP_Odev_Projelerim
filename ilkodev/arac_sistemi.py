from datetime import datetime

class Arac:
    def __init__(self, arac_id, marka, model, kilometre):
        self.arac_id = arac_id
        self.marka = marka
        self.model = model
        self.kilometre = kilometre
        self.musait_mi = True

    def arac_durumu_guncelle(self, durum):
        self.musait_mi = durum

    def kilometre_guncelle(self, yeni_km):
        self.kilometre += yeni_km

class Kullanici:
    def __init__(self, kullanici_id, ad, ehliyet_no):
        self.kullanici_id = kullanici_id
        self.ad = ad
        self.ehliyet_no = ehliyet_no
        self.gecmis = []

    def kiralama_gecmisi_ekle(self, kiralama_bilgisi):
        self.gecmis.append(kiralama_bilgisi)

class Kiralama:
    def __init__(self, kiralama_id, arac, kullanici):
        self.kiralama_id = kiralama_id
        self.arac = arac
        self.kullanici = kullanici
        self.baslangic_saati = None
        self.bitis_saati = None

    def kiralama_baslat(self):
        if self.arac.musait_mi:
            self.baslangic_saati = datetime.now()
            self.arac.arac_durumu_guncelle(False)
            print(f"\n {self.arac.marka} kiralama işlemi başlatıldı.")
        else:
            print("\n Bu araç şu an müsait değil!")

    def kiralama_bitir(self, gidilen_km):
        self.bitis_saati = datetime.now()
        self.arac.arac_durumu_guncelle(True)
        self.arac.kilometre_guncelle(gidilen_km)
        self.kullanici.kiralama_gecmisi_ekle(f"ID: {self.kiralama_id}, Araç: {self.arac.marka}")
        print(f"\n Kiralama bitti. Araç {gidilen_km} km yol yaptı.")


if __name__ == "__main__":
    arac1 = Arac(1, "Tesla", "Model 3", 10000)
    arac2 = Arac(2, "BMW", "i4", 5000)
    araclar = {1: arac1, 2: arac2}
    
    kullanici = Kullanici(1, "İbrahim Efe", "ABC123")
    aktif_kiralama = None

    while True:
        print("\n--- ARAÇ PAYLAŞIM SİSTEMİ ---")
        print("1. Araçları Listele")
        print("2. Araç Kirala")
        print("3. Aracı Teslim Et")
        print("4. Çıkış")
        
        secim = input("Lütfen yapmak istediğiniz işlemi seçin: ")

        if secim == "1":
            print("\n--- ARAÇ LİSTESİ ---")
            for id, a in araclar.items():
                durum = "Müsait" if a.musait_mi else "Kirada"
                print(f"ID: {id} | {a.marka} {a.model} | KM: {a.kilometre} | Durum: {durum}")
        
        elif secim == "2":
            if aktif_kiralama and not aktif_kiralama.arac.musait_mi:
                print("\n Zaten bir aracınız var, önce onu teslim edin!")
            else:
                arac_id = int(input("Kiralamak istediğiniz aracın ID'sini girin: "))
                if arac_id in araclar:
                    aktif_kiralama = Kiralama(101, araclar[arac_id], kullanici)
                    aktif_kiralama.kiralama_baslat()
                else:
                    print("\n Geçersiz Araç ID!")

        elif secim == "3":
            if aktif_kiralama and not aktif_kiralama.arac.musait_mi:
                km = int(input("Kaç km yol yaptınız?: "))
                aktif_kiralama.kiralama_bitir(km)
            else:
                print("\n Kirada olan bir aracınız bulunmuyor!")

        elif secim == "4":
            print("Sistemden çıkılıyor... İyi Günler!")
            break
        else:
            print("Geçersiz seçim, lütfen tekrar deneyin.")
