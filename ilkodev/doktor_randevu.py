import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime

class Hasta:
    def __init__(self, hasta_id, ad, tc, telefon):
        self.hasta_id = hasta_id
        self.ad = ad
        self.tc = tc
        self.telefon = telefon
        self.randevularim = []

    def randevu_al(self, randevu_dict):
        self.randevularim.append(randevu_dict)

class Doktor:
    def __init__(self, doktor_id, ad, uzmanlik):
        self.doktor_id = doktor_id
        self.ad = ad
        self.uzmanlik = uzmanlik
        self.randevu_takvimi = {}

    def uygunluk_kontrol(self, tarih, saat):
        if tarih not in self.randevu_takvimi:
            self.randevu_takvimi[tarih] = {
                "09:00": True, "10:00": True, "11:00": True, 
                "13:00": True, "14:00": True, "15:00": True
            }
        return self.randevu_takvimi[tarih].get(saat, False)

class RandevuUygulamasi:
    def __init__(self, root):
        self.root = root
        self.root.title("İKÜ Sağlık - Tarihli Randevu Sistemi")
        self.root.geometry("600x750")
        self.root.configure(bg="#f8f9fa")

        self.doktorlar = {
            "1": Doktor(1, "Oğulcan Akın", "Kardiyoloji"),
            "2": Doktor(2, "Yusuf Udum", "Göz Hastalıkları"),
            "3": Doktor(3, "Ayşe Yılmaz", "Dahiliye")
        }
        self.mevcut_hasta = Hasta(101, "İbrahim Efe", "12345678901", "5423549363")

        self.arayuz_tasarla()

    def arayuz_tasarla(self):
        tk.Label(self.root, text="DOKTOR RANDEVU SİSTEMİ", font=("Segoe UI", 18, "bold"), bg="#f8f9fa", fg="#343a40").pack(pady=20)

        frame_form = tk.LabelFrame(self.root, text="Randevu Bilgileri", padx=15, pady=15, bg="white", font=("Segoe UI", 10, "bold"))
        frame_form.pack(fill="x", padx=25, pady=10)

        tk.Label(frame_form, text="Doktor:", bg="white").grid(row=0, column=0, sticky="w", pady=8)
        self.combo_doktor = ttk.Combobox(frame_form, values=[f"{d.ad} ({d.uzmanlik})" for d in self.doktorlar.values()], state="readonly", width=30)
        self.combo_doktor.grid(row=0, column=1, pady=8, padx=10)
        self.combo_doktor.bind("<<ComboboxSelected>>", self.formu_guncelle)

        tk.Label(frame_form, text="Tarih:", bg="white").grid(row=1, column=0, sticky="w", pady=8)
        self.cal = DateEntry(frame_form, width=28, background='darkblue', foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy', mindate=datetime.now())
        self.cal.grid(row=1, column=1, pady=8, padx=10)
        self.cal.bind("<<DateEntrySelected>>", self.formu_guncelle)

        tk.Label(frame_form, text="Saat:", bg="white").grid(row=2, column=0, sticky="w", pady=8)
        self.combo_saat = ttk.Combobox(frame_form, state="readonly", width=30)
        self.combo_saat.grid(row=2, column=1, pady=8, padx=10)

        tk.Button(frame_form, text="Randevuyu Kaydet", command=self.randevu_kaydet_cmd, bg="#007bff", fg="white", font=("Segoe UI", 10, "bold")).grid(row=3, column=0, columnspan=2, pady=15, sticky="we")

        frame_liste = tk.LabelFrame(self.root, text="Aktif Randevularınız", padx=15, pady=15, bg="white", font=("Segoe UI", 10, "bold"))
        frame_liste.pack(fill="both", expand=True, padx=25, pady=10)

        self.listbox_randevular = tk.Listbox(frame_liste, font=("Consolas", 10), height=10)
        self.listbox_randevular.pack(fill="both", expand=True, pady=5)
        
        tk.Button(frame_liste, text="Seçili Randevuyu İptal Et", command=self.randevu_iptal_cmd, bg="#dc3545", fg="white", font=("Segoe UI", 10, "bold")).pack(fill="x", pady=5)
        
        self.randevu_listesini_yenile()

    def formu_guncelle(self, event=None):
        """Hem doktor hem tarih değiştiğinde saat listesini yeniler."""
        dr_metin = self.combo_doktor.get()
        tarih = self.cal.get()
        
        if not dr_metin: return
        
        dr_ad = dr_metin.split(" (")[0]
        for dr in self.doktorlar.values():
            if dr.ad == dr_ad:
                if tarih not in dr.randevu_takvimi:
                    dr.randevu_takvimi[tarih] = {"09:00": True, "10:00": True, "11:00": True, "13:00": True, "14:00": True, "15:00": True}
                
                musaitler = [s for s, durum in dr.randevu_takvimi[tarih].items() if durum]
                self.combo_saat['values'] = musaitler
                self.combo_saat.set("")
                break

    def randevu_kaydet_cmd(self):
        dr_bilgisi = self.combo_doktor.get()
        tarih = self.cal.get()
        saat = self.combo_saat.get()

        if not dr_bilgisi or not saat:
            messagebox.showwarning("Uyarı", "Lütfen tüm seçimleri yapın!")
            return

        dr_ad = dr_bilgisi.split(" (")[0]
        for dr in self.doktorlar.values():
            if dr.ad == dr_ad:
                if dr.uygunluk_kontrol(tarih, saat):
                    dr.randevu_takvimi[tarih][saat] = False
                    self.mevcut_hasta.randevu_al({
                        "gorunum": f"{tarih} - {saat} | Dr. {dr.ad}",
                        "dr_obj": dr,
                        "tarih": tarih,
                        "saat": saat
                    })
                    messagebox.showinfo("Onay", "Randevunuz başarıyla kaydedildi.")
                    self.formu_guncelle()
                    self.randevu_listesini_yenile()
                    return

    def randevu_iptal_cmd(self):
        secili = self.listbox_randevular.curselection()
        if not secili:
            messagebox.showwarning("Hata", "Lütfen iptal edilecek randevuyu seçin.")
            return

        if messagebox.askyesno("İptal", "Bu randevuyu iptal etmek istiyor musunuz?"):
            r = self.mevcut_hasta.randevularim.pop(secili[0])
            r["dr_obj"].randevu_takvimi[r["tarih"]][r["saat"]] = True
            messagebox.showinfo("Bilgi", "Randevunuz iptal edildi.")
            self.randevu_listesini_yenile()
            self.formu_guncelle()

    def randevu_listesini_yenile(self):
        self.listbox_randevular.delete(0, tk.END)
        for r in self.mevcut_hasta.randevularim:
            self.listbox_randevular.insert(tk.END, r["gorunum"])

if __name__ == "__main__":
    root = tk.Tk()
    app = RandevuUygulamasi(root)
    root.mainloop()
    
