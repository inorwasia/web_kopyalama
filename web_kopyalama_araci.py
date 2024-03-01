import os
import requests
from bs4 import BeautifulSoup
from tkinter import messagebox
from urllib.parse import urljoin
import tkinter as tk
from tkinter import ttk
import threading
import pygame
import time

# Pygame'i başlat
pygame.init()
pygame.mixer.init()

# Ses dosyasını yükle
button_sound = pygame.mixer.Sound("0301.wav")

def kopyala_web_sitesi(url, klasor_adi="web_sitesi"):
    try:
        # Kullanıcı ajanını tanımla
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"}
        
        # URL'den web sitesi içeriğini al
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            # BeautifulSoup kullanarak web sitesi içeriğini işle
            soup = BeautifulSoup(response.content, 'html.parser')

            # Klasör oluştur
            if not os.path.exists(klasor_adi):
                os.makedirs(klasor_adi)

            # HTML dosyasını kaydet
            with open(os.path.join(klasor_adi, "index.html"), "w", encoding="utf-8") as f:
                f.write(response.text)

            # CSS dosyalarını kaydet
            css_links = soup.find_all("link", rel="stylesheet")
            for css_link in css_links:
                css_url = urljoin(url, css_link["href"])
                css_response = requests.get(css_url, headers=headers)
                if css_response.status_code == 200:
                    with open(os.path.join(klasor_adi, os.path.basename(css_url)), "wb") as f:
                        f.write(css_response.content)

            # Resim dosyalarını kaydet
            img_tags = soup.find_all("img")
            for img_tag in img_tags:
                img_url = urljoin(url, img_tag["src"])
                img_response = requests.get(img_url, headers=headers)
                if img_response.status_code == 200:
                    with open(os.path.join(klasor_adi, os.path.basename(img_url)), "wb") as f:
                        f.write(img_response.content)

            messagebox.showinfo("Başarılı", "Web sitesi başarıyla kopyalandı.")
        else:
            messagebox.showerror("Hata", "Sayfa alınamadı. Hata kodu: " + str(response.status_code))
    except Exception as e:
        messagebox.showerror("Hata", "Bir hata oluştu: " + str(e))

def kopyala_ve_bekle(url):
    loading_label.config(text="Inorwa başlatılıyor, lütfen bekleyin...", font=("Helvetica", 10, "italic"), foreground="gray")
    kopyala_web_sitesi(url)
    loading_label.config(text="Inorwa başlatıldı", font=("Helvetica", 10), foreground="black")
    time.sleep(2)  # 2 saniye bekle
    loading_label.config(text="", font=("Helvetica", 10), foreground="black")

def kopyala_thread():
    url = url_giris.get()
    threading.Thread(target=kopyala_ve_bekle, args=(url,)).start()

def play_sound(event=None):
    button_sound.play()

# Tkinter penceresini oluştur
root = tk.Tk()
root.title("Inorwa")  # Uygulama adını "Inorwa" olarak değiştir

# Uygulama simgesini "inorwa.ico" olarak değiştir
root.iconbitmap("inorwa.ico")

# Uygulama temasını dark yap
root.configure(bg="#020410")  # Arka plan rengini siyah yap

# Logo görüntüsünü ekle
logo_image = tk.PhotoImage(file="logo.png")
logo_label = tk.Label(root, image=logo_image, bg="#020410")
logo_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

# "Inorwa başlatılıyor, lütfen bekleyin..." yazısı
loading_label = ttk.Label(root, text="Inorwa başlatılıyor, lütfen bekleyin...", background="#020410", foreground="white")
loading_label.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

# URL giriş kutusu
url_etiket = ttk.Label(root, text="URL:", background="#020410", foreground="white")
url_etiket.grid(row=2, column=0, padx=5, pady=5)
url_giris = ttk.Entry(root, width=50)
url_giris.grid(row=2, column=1, padx=5, pady=5)

# Kopyala düğmesi
kopyala_dugme = ttk.Button(root, text="Kopyala", command=kopyala_thread, style="DarkButton.TButton")
kopyala_dugme.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Stil oluştur
style = ttk.Style()
style.configure("DarkButton.TButton", background="#090b1a", foreground="white", font=("Helvetica", 10, "bold"))

# Olayları bağlama
kopyala_dugme.bind("<Enter>", play_sound)

# Pencereyi başlat
root.mainloop()
