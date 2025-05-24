# Gerekli kütüphaneler
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import matplotlib.pyplot as plt
from skfuzzy.control import ControlSystemSimulation

# --- Fuzzy Değişkenler ---

# Inputlar
ic_sicaklik = ctrl.Antecedent(np.arange(15, 36, 1), 'ic_sicaklik')
dis_sicaklik = ctrl.Antecedent(np.arange(0, 41, 1), 'dis_sicaklik')
delta_sicaklik = ctrl.Antecedent(np.arange(-5, 6, 1), 'delta_sicaklik')
nem = ctrl.Antecedent(np.arange(20, 101, 1), 'nem')
saat = ctrl.Antecedent(np.arange(0, 4, 1), 'saat')

# Outputlar
klima_ayari = ctrl.Consequent(np.arange(18, 31, 1), 'klima_ayari')
fan_seviyesi = ctrl.Consequent(np.arange(0, 101, 1), 'fan_seviyesi')

# --- Membership Functions ---

ic_sicaklik.automf(3)
dis_sicaklik.automf(3)
delta_sicaklik['dusuyor'] = fuzz.trimf(delta_sicaklik.universe, [-5, -3, 0])
delta_sicaklik['sabit'] = fuzz.trimf(delta_sicaklik.universe, [-1, 0, 1])
delta_sicaklik['artiyor'] = fuzz.trimf(delta_sicaklik.universe, [0, 3, 5])

nem['dusuk'] = fuzz.trimf(nem.universe, [20, 30, 50])
nem['orta'] = fuzz.trimf(nem.universe, [40, 60, 80])
nem['yuksek'] = fuzz.trimf(nem.universe, [70, 85, 100])

saat['gece'] = fuzz.trimf(saat.universe, [0, 0, 1])
saat['sabah'] = fuzz.trimf(saat.universe, [0, 1, 2])
saat['oglen'] = fuzz.trimf(saat.universe, [1, 2, 3])
saat['aksam'] = fuzz.trimf(saat.universe, [2, 3, 3])

klima_ayari['dusuk'] = fuzz.trimf(klima_ayari.universe, [18, 20, 22])
klima_ayari['orta'] = fuzz.trimf(klima_ayari.universe, [21, 24, 27])
klima_ayari['yuksek'] = fuzz.trimf(klima_ayari.universe, [26, 28, 30])

fan_seviyesi['dusuk'] = fuzz.trimf(fan_seviyesi.universe, [0, 20, 40])
fan_seviyesi['orta'] = fuzz.trimf(fan_seviyesi.universe, [30, 50, 70])
fan_seviyesi['yuksek'] = fuzz.trimf(fan_seviyesi.universe, [60, 80, 100])

# --- Kurallar ---
rules = [
    # Genişletilmiş detaylı kurallar
    ctrl.Rule(ic_sicaklik['poor'] & dis_sicaklik['poor'] & delta_sicaklik['artiyor'], klima_ayari['yuksek']),
    ctrl.Rule(ic_sicaklik['poor'] & dis_sicaklik['average'] & delta_sicaklik['artiyor'], klima_ayari['yuksek']),
    ctrl.Rule(ic_sicaklik['poor'] & dis_sicaklik['good'] & delta_sicaklik['sabit'], klima_ayari['orta']),
    ctrl.Rule(ic_sicaklik['average'] & delta_sicaklik['artiyor'] & saat['oglen'], klima_ayari['yuksek']),
    ctrl.Rule(ic_sicaklik['average'] & delta_sicaklik['dusuyor'] & saat['gece'], klima_ayari['dusuk']),
    ctrl.Rule(ic_sicaklik['good'] & nem['yuksek'], klima_ayari['dusuk']),
    ctrl.Rule(ic_sicaklik['good'] & dis_sicaklik['poor'], klima_ayari['dusuk']),

    ctrl.Rule(ic_sicaklik['poor'] & nem['yuksek'] & saat['oglen'], fan_seviyesi['yuksek']),
    ctrl.Rule(ic_sicaklik['average'] & nem['orta'] & saat['aksam'], fan_seviyesi['orta']),
    ctrl.Rule(ic_sicaklik['good'] & nem['dusuk'] & saat['gece'], fan_seviyesi['dusuk']),
    ctrl.Rule(ic_sicaklik['poor'] & delta_sicaklik['artiyor'], fan_seviyesi['yuksek']),
    ctrl.Rule(ic_sicaklik['average'] & delta_sicaklik['sabit'], fan_seviyesi['orta']),
    ctrl.Rule(ic_sicaklik['good'] & delta_sicaklik['dusuyor'], fan_seviyesi['dusuk']),
    # Ekstra genel kurallar
    ctrl.Rule(ic_sicaklik['average'], klima_ayari['orta']),
    ctrl.Rule(nem['orta'], klima_ayari['orta']),
    ctrl.Rule(dis_sicaklik['average'], klima_ayari['orta']),
    ctrl.Rule(ic_sicaklik['average'], fan_seviyesi['orta']),
    ctrl.Rule(nem['orta'], fan_seviyesi['orta']),
    ctrl.Rule(dis_sicaklik['average'], fan_seviyesi['orta']),
    ctrl.Rule(ic_sicaklik['poor'] & dis_sicaklik['good'], klima_ayari['yuksek']),
    ctrl.Rule(ic_sicaklik['average'] & nem['yuksek'], klima_ayari['orta']),
    ctrl.Rule(ic_sicaklik['good'] & nem['dusuk'], klima_ayari['dusuk']),
    ctrl.Rule(delta_sicaklik['artiyor'], klima_ayari['yuksek']),
    ctrl.Rule(delta_sicaklik['dusuyor'], klima_ayari['dusuk']),
    ctrl.Rule(saat['oglen'] & ic_sicaklik['poor'], klima_ayari['yuksek']),

    ctrl.Rule(ic_sicaklik['poor'] & nem['yuksek'], fan_seviyesi['yuksek']),
    ctrl.Rule(ic_sicaklik['average'] & nem['orta'], fan_seviyesi['orta']),
    ctrl.Rule(ic_sicaklik['good'] & nem['dusuk'], fan_seviyesi['dusuk']),
    ctrl.Rule(delta_sicaklik['artiyor'], fan_seviyesi['yuksek']),
    ctrl.Rule(saat['aksam'] & ic_sicaklik['average'], fan_seviyesi['orta']),
    ctrl.Rule(saat['gece'] & ic_sicaklik['good'], fan_seviyesi['dusuk'])
]

# --- Kontrol Sistemi ---
klima_ctrl = ctrl.ControlSystem(rules)

# --- Main Fonksiyon (GUI) ---
def main():
    hesaplandi = {'tamam': False}
    def hesapla():
        hesaplandi['tamam'] = False
        try:
            # Girişleri al
            ic = float(entry_ic.get())
            dis = float(entry_dis.get())
            delta = float(entry_delta.get())
            n = float(entry_nem.get())
            s = float(entry_saat.get())

            # Aralık kontrolleri
            if not (15 <= ic <= 35):
                raise ValueError("İç sıcaklık 15-35 aralığında olmalıdır.")
            if not (0 <= dis <= 40):
                raise ValueError("Dış sıcaklık 0-40 aralığında olmalıdır.")
            if not (-5 <= delta <= 5):
                raise ValueError("Δ Sıcaklık -5 ile 5 arasında olmalıdır.")
            if not (20 <= n <= 100):
                raise ValueError("Nem 20-100 aralığında olmalıdır.")
            if not (0 <= s <= 3):
                raise ValueError("Saat 0 ile 3 arasında olmalıdır (0: Gece, 3: Akşam).")
            # Yeni simülasyon nesnesi
            klima_sim = ctrl.ControlSystemSimulation(klima_ctrl)

            # Girişleri al ve kontrol et
            ic = float(entry_ic.get())
            dis = float(entry_dis.get())
            delta = float(entry_delta.get())
            n = float(entry_nem.get())
            s = float(entry_saat.get())

            klima_sim.input['ic_sicaklik'] = ic
            klima_sim.input['dis_sicaklik'] = dis
            klima_sim.input['delta_sicaklik'] = delta
            klima_sim.input['nem'] = n
            klima_sim.input['saat'] = s

            klima_sim.compute()

            klima_ayari_output = klima_sim.output.get('klima_ayari', None)
            fan_seviyesi_output = klima_sim.output.get('fan_seviyesi', None)

            if klima_ayari_output is not None and fan_seviyesi_output is not None:
                hesaplandi['tamam'] = True
                lbl_klima.config(text=f"Klima Ayarı: {klima_ayari_output:.1f} C")
                lbl_fan.config(text=f"Fan Seviyesi: {fan_seviyesi_output:.1f} %")
            else:
                messagebox.showerror("Hata", "Fuzzy işlem sonucu boş. Girdileri kontrol et.")

        except ValueError:
            messagebox.showerror("Hata", "Lütfen tüm alanlara geçerli sayılar girin.")
        except Exception as e:
            messagebox.showerror("Hata", str(e))

    root = tk.Tk()
    root.title("Bina İçi Klima Fuzzy Kontrol")

    ttk.Label(root, text="İç Sıcaklık (15-35)").grid(row=0, column=0)
    entry_ic = ttk.Entry(root)
    entry_ic.bind('<KeyRelease>', lambda e: hesaplandi.update({'tamam': False}))
    entry_ic.grid(row=0, column=1)

    ttk.Label(root, text="Dış Sıcaklık (0-40)").grid(row=1, column=0)
    entry_dis = ttk.Entry(root)
    entry_dis.bind('<KeyRelease>', lambda e: hesaplandi.update({'tamam': False}))
    entry_dis.grid(row=1, column=1)

    ttk.Label(root, text="Δ Sıcaklık (-5 ila 5)").grid(row=2, column=0)
    entry_delta = ttk.Entry(root)
    entry_delta.bind('<KeyRelease>', lambda e: hesaplandi.update({'tamam': False}))
    entry_delta.grid(row=2, column=1)

    ttk.Label(root, text="Nem (%)").grid(row=3, column=0)
    entry_nem = ttk.Entry(root)
    entry_nem.bind('<KeyRelease>', lambda e: hesaplandi.update({'tamam': False}))
    entry_nem.grid(row=3, column=1)

    ttk.Label(root, text="Saat (0: Gece, 1: Sabah, 2: Öğlen, 3: Akşam)").grid(row=4, column=0)
    entry_saat = ttk.Entry(root)
    entry_saat.bind('<KeyRelease>', lambda e: hesaplandi.update({'tamam': False}))
    entry_saat.grid(row=4, column=1)

    ttk.Button(root, text="Hesapla", command=hesapla).grid(row=5, column=0, columnspan=2)
    lbl_klima = ttk.Label(root, text="Klima Ayarı: ")
    lbl_klima.grid(row=6, column=0, columnspan=2)
    lbl_fan = ttk.Label(root, text="Fan Seviyesi: ")
    lbl_fan.grid(row=7, column=0, columnspan=2)

    def goster_grafikler():
        if not hesaplandi['tamam']:
            messagebox.showinfo("Uyarı", "Lütfen önce geçerli bir sonuç hesaplayınız.")
            return

        sim = ControlSystemSimulation(klima_ctrl)

        try:
            sim.input['ic_sicaklik'] = float(entry_ic.get())
            sim.input['dis_sicaklik'] = float(entry_dis.get())
            sim.input['delta_sicaklik'] = float(entry_delta.get())
            sim.input['nem'] = float(entry_nem.get())
            sim.input['saat'] = float(entry_saat.get())
            sim.compute()
        except:
            messagebox.showerror("Hata", "Grafik çizimi için hesaplama yapılamadı.")
            return

        ic_sicaklik.view(sim=sim)
        dis_sicaklik.view(sim=sim)
        delta_sicaklik.view(sim=sim)
        nem.view(sim=sim)
        saat.view(sim=sim)

        klima_ayari.view(sim=sim)
        fan_seviyesi.view(sim=sim)

        plt.show()

    ttk.Button(root, text="Grafikleri Göster", command=goster_grafikler).grid(row=8, column=0, columnspan=2)
    root.mainloop()

if __name__ == '__main__':
    main()

