import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Sacın özellikleri
sac_kalinlik = 20  # mm
sac_uzunluk = 100  # mm (isteğe bağlı, sacın uzunluğu)

# Torç ve ışın özellikleri
torc_genislik = 10  # mm
torc_boyu = 60  # mm
torc_yukseklik = sac_kalinlik + 6  # mm (sacın 3 mm üzerinde)
torc_konum = (sac_uzunluk - torc_genislik / 2, torc_yukseklik)  # Torcun ortası sacın ucunda
isin_uzunluk = sac_kalinlik + 10  # Işının sacın altından 10 mm çıkması

# Grafik oluşturma
fig, ax = plt.subplots(figsize=(10, 6))
plt.xlim(-10, sac_uzunluk + 20)
plt.ylim(-10, torc_yukseklik + torc_boyu + 10)

# Sacı çizme
plt.plot([0, sac_uzunluk], [0, 0], 'b-', linewidth=5, label="Sac")
plt.plot([0, sac_uzunluk], [sac_kalinlik, sac_kalinlik], 'b-', linewidth=5)

# Torcu çizme (dikdörtgen)
torc = patches.Rectangle(torc_konum, torc_genislik, torc_boyu, linewidth=2, edgecolor='k', facecolor='none', label="Torç")
ax.add_patch(torc)

# Işını çizme
plt.plot([torc_konum[0] + torc_genislik / 2, torc_konum[0] + torc_genislik / 2], [torc_konum[1] + torc_boyu, -isin_uzunluk], 'r--', label="Plazma Işını")

# Açıklamalar
plt.text(sac_uzunluk / 2, -5, f"Sac Kalınlığı: {sac_kalinlik} mm", ha='center', va='top')

# Grafik ayarları
plt.xlabel("X (mm)")
plt.ylabel("Y (mm)")
plt.title("Plazma Kesme Torcu ve Sac Simülasyonu")
plt.legend()
plt.grid(True)
plt.show()
