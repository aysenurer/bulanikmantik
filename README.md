# 🧠 Akıllı Klima Kontrol Sistemi (Fuzzy Logic)

Bu proje, Python programlama dili ile geliştirilmiş, bulanık mantık (fuzzy logic) kullanarak bir ev/ofis ortamında klima kontrolünü otomatikleştiren bir sistemdir. Kullanıcıdan alınan sıcaklık, nem, zaman gibi çevresel veriler ile klima sıcaklığı ve fan seviyesi hesaplanmaktadır.

## 🚀 Projeyi Çalıştırmak

Aşağıdaki adımları takip ederek projeyi bilgisayarınıza indirip çalıştırabilirsiniz:

### 1. Reponun Klonlanması

```bash
git clone https://github.com/KULLANICIADI/projeismi.git
cd akilli-klima-fuzzy
```

### 2. Gerekli Kütüphanelerin Kurulumu

Python yüklü değilse [python.org](https://www.python.org/) üzerinden kurun. Ardından terminal veya komut satırına:

```bash
pip install -r requirements.txt
```

### 3. Uygulamayı Başlatmak

```bash
python main.py
```

Tkinter arayüzü açıldığında, gerekli değerleri girip "Hesapla" ve ardından "Grafikleri Göster" butonlarına basabilirsiniz.

## 💡 Sistem Girdileri

- İç Sıcaklık (15 - 35 °C)
- Dış Sıcaklık (0 - 40 °C)
- Sıcaklık Değişim Hızı (-5 ila +5)
- Nem (%20 - %100)
- Saat (0: Gece, 1: Sabah, 2: Öğlen, 3: Akşam)

## 🎯 Sistem Çıktıları

- Klima sıcaklık ayarı (18 - 30 °C arası)
- Fan seviyesi (%0 - %100)

## 📚 Kullanılan Teknolojiler

- Python
- scikit-fuzzy
- matplotlib
- tkinter

## 📝 Lisans

MIT Lisansı. Açık kaynak kodludur, dilediğiniz gibi kullanabilirsiniz.
