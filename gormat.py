import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Sacın özellikleri
sac_kalinlik = 20  # mm
sac_uzunluk = 100  # mm



# Torç ve ışın özellikleri
torc_genislik = 10  # mm
torc_boyu = 60  # mm
torc_yukseklik = sac_kalinlik + 6  # mm (sacın 3 mm üzerinde)
torc_konum = (sac_uzunluk - torc_genislik / 2, torc_yukseklik)  # Torcun ortası sacın ucunda
#isin_uzunluk = sac_kalinlik + 10  # Işının sacın altından 10 mm çıkması
#isin_konum = (sac_uzunluk - torc_genislik / 2, torc_yukseklik-10)  # Torcun ortası sacın ucunda


# Grafik oluşturma
fig, ax = plt.subplots(figsize=(10, 6))
plt.xlim(-10, sac_uzunluk + 20)
plt.ylim(-10, torc_yukseklik + torc_boyu + 10)

# Sacı çizme
plt.plot([0, sac_uzunluk], [0, 0], 'b-', linewidth=5, label="Sac")
plt.plot([0, sac_uzunluk], [sac_kalinlik, sac_kalinlik], 'b-', linewidth=5)

# Torç ve ışın grafikleri
torc = patches.Rectangle(torc_konum, torc_genislik, torc_boyu, linewidth=2, edgecolor='k', facecolor='none', label="Torç")
ax.add_patch(torc)


beam_line, = plt.plot([], [], 'r--', label="Plazma Işını")
angle_text = plt.text(0, 0, "", ha='right', va='bottom')
slope_text = plt.text(0, 0, "", ha='left', va='top')

# Başlangıç açısı (derece cinsinden)
aci = 0

# Grafikleri güncelleme fonksiyonu
def update_plot(aci):
    radyan = np.radians(aci)

    # Torcun dönme noktası (alt orta nokta)
    donme_noktasi_x = sac_uzunluk - torc_genislik / 2
    donme_noktasi_y = torc_yukseklik

    # Torcun konumu (dönme noktasına göre hesaplanır)
    torc_x = donme_noktasi_x - torc_boyu * np.sin(radyan)
    torc_y = donme_noktasi_y + torc_boyu * np.cos(radyan)
    torc.set_xy((torc_x, torc_y))
    torc.angle = aci  # Açıyı pozitif kullan

    # Işının uzunluğu (sacın altından 10 mm çıkacak şekilde)
    isin_uzunluk = sac_kalinlik + 10

    # Işını çizme (dönme noktasından başlar)
    beam_line.set_data(
        [donme_noktasi_x, donme_noktasi_x - isin_uzunluk * np.cos(radyan)],  # Işının x koordinatları
        [donme_noktasi_y, donme_noktasi_y - isin_uzunluk * np.sin(radyan)],  # Işının y koordinatları
    )

    # Açıklamaları güncelle
    angle_text.set_text(f"Torç ({aci}°)")
    angle_text.set_position((torc_x, torc_y))
    slope_text.set_text(f"Eğim ({aci:.1f}°)")
    slope_text.set_position((sac_uzunluk, sac_kalinlik))

    fig.canvas.draw_idle()

# İlk çizim
update_plot(aci)

# Mouse click olayını yakalama fonksiyonu
def onclick(event):
    global aci
    if event.inaxes:
        aci = np.degrees(np.arctan2(event.ydata - torc_yukseklik, event.xdata - (sac_uzunluk - torc_genislik / 2)))
        update_plot(aci)

# Mouse click olayını bağlama
plt.connect('button_press_event', onclick)

# Açıklamalar
plt.text(sac_uzunluk / 2, -5, f"Sac Kalınlığı: {sac_kalinlik} mm", ha='center', va='top')

# Grafik ayarları
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("Plazma Kesme Torcu ve Sac Simülasyonu")
plt.legend()

plt.show()
