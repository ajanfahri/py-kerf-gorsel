import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Torç ve sacın başlangıç konumları
torc_x, torc_y = 0, 10
sac_x, sac_y = 0, 0
sac_kalinlik = 20

# Başlangıç açısı (derece cinsinden)
aci = st.slider("Torç Açısı (Derece)", min_value=0, max_value=90, value=45)

# Grafik oluşturma
fig, ax = plt.subplots(figsize=(8, 6))
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.axis('equal')

# Torç ışını ve sac grafikleri
beam_line, = plt.plot([], [], 'r-', label="Plazma Işını")
plate_line, = plt.plot([sac_x, sac_x], [sac_y, sac_y + sac_kalinlik], 'b-', label="Sac")
angle_text = plt.text(torc_x, torc_y, "", ha='right', va='bottom')
slope_text = plt.text(sac_x, sac_y + sac_kalinlik, "", ha='left', va='top')

# Açıyı radyana çevir
radyan = np.radians(aci)

# Işının sacla kesiştiği noktayı hesapla
kesisim_x = sac_x
kesisim_y = sac_y + sac_kalinlik

# Eğim açısını hesapla
egim_radyan = np.arctan2(kesisim_y - torc_y, kesisim_x - torc_x)
egim_aci = np.degrees(egim_radyan)

# Grafikleri güncelle (ilk çizim)
beam_line.set_data([torc_x, kesisim_x], [torc_y, kesisim_y])
angle_text.set_text(f"Torç ({aci}°)")
slope_text.set_text(f"Eğim ({egim_aci:.1f}°)")

# Grafiği Streamlit uygulamasında göster
st.pyplot(fig)
