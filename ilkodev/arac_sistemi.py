import tkinter as tk
from tkinter import messagebox
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

class AracKiralamaUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("Araç Paylaşım Sistemi")
        self.root.geometry("500x600")

        self.araclar = {
            1: Arac(1, "Tesla", "Model 3", 10000),
            2: Arac(2, "BMW", "i4", 5000),
            3: Arac(3, "Volkswagen", "Golf", 12000)
        }
        self.kullanici = Kullanici(1, "İbrahim Efe", "ABC123")
        self.aktif_kiralama = None

        self.arayuz_olustur()

    def arayuz_olustur(self):

        tk.Label(self.root, text="--- ARAÇ PAYLAŞIM SİSTEMİ ---", font=("Arial", 14, "bold")).pack(pady=10)

        frame_liste = tk.LabelFrame(self.root, text="Mevcut Araçlar", padx=10, pady=10)
        frame_liste.pack(fill="both", padx=10, pady=5)

        self.text_liste = tk.Text(frame_liste, height=8, width=55)
        self.text_liste.pack()
        self.liste_guncelle()

        frame_islem = tk.LabelFrame(self.root, text="Kiralama İşlemleri", padx=10, pady=10)
        frame_islem.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_islem, text="Araç ID:").grid(row=0, column=0, sticky="w")
        self.entry_arac_id = tk.Entry(frame_islem)
        self.entry_arac_id.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_islem, text="Aracı Kirala", command=self.kirala_cmd, bg="green", fg="white").grid(row=0, column=2, padx=5)

        frame_teslim = tk.LabelFrame(self.root, text="Teslim İşlemleri", padx=10, pady=10)
        frame_teslim.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_teslim, text="Gidilen KM:").grid(row=0, column=0, sticky="w")
        self.entry_km = tk.Entry(frame_teslim)
        self.entry_km.grid(row=0, column=1, padx=5, pady=5)

        tk.Button(frame_teslim, text="Aracı Teslim Et", command=self.teslim_et_cmd, bg="blue", fg="white").grid(row=0, column=2, padx=5)

    def liste_guncelle(self):
        self.text_liste.delete(1.0, tk.END)
        for id, a in self.araclar.items():
            durum = "MÜSAİT" if a.musait_mi else "KİRADA"
            satir = f"ID: {id} | {a.marka} {a.model} | KM: {a.kilometre} | [{durum}]\n"
            self.text_liste.insert(tk.END, satir)

    def kirala_cmd(self):
        try:
            secilen_id = int(self.entry_arac_id.get())
            if self.aktif_kiralama and not self.aktif_kiralama["musait"]:
                messagebox.showwarning("Uyarı", "Zaten aktif bir kiralamanız var!")
                return

            if secilen_id in self.araclar:
                arac = self.araclar[secilen_id]
                if arac.musait_mi:
                    arac.arac_durumu_guncelle(False)
                    self.aktif_kiralama = {"arac": arac, "musait": False, "baslangic": datetime.now()}
                    messagebox.showinfo("Başarılı", f"{arac.marka} başarıyla kiralandı.")
                    self.liste_guncelle()
                else:
                    messagebox.showerror("Hata", "Bu araç şu an kirada!")
            else:
                messagebox.showerror("Hata", "Geçersiz Araç ID!")
        except ValueError:
            messagebox.showwarning("Hata", "Lütfen geçerli bir sayısal ID girin.")

    def teslim_et_cmd(self):
        if not self.aktif_kiralama:
            messagebox.showwarning("Uyarı", "Teslim edilecek aktif bir araç yok!")
            return

        try:
            gidilen_km = int(self.entry_km.get())
            arac = self.aktif_kiralama["arac"]
            
            arac.arac_durumu_guncelle(True)
            arac.kilometre_guncelle(gidilen_km)
            
            messagebox.showinfo("Teslim Edildi", f"Araç teslim alındı.\nToplam KM: {arac.kilometre}")
            
            self.aktif_kiralama = None
            self.entry_km.delete(0, tk.END)
            self.liste_guncelle()
        except ValueError:
            messagebox.showwarning("Hata", "Lütfen gidilen kilometreyi sayı olarak girin.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AracKiralamaUygulamasi(root)
    root.mainloop()
