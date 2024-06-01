import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import matplotlib.transforms as transforms

# Sayfa başlığı
st.title("TEST")


# Açı kontrolü için progress bar
gelenaci = st.slider("Torç Açısı (Derece)", min_value=-45, max_value=45, value=0)


sac_kalinlik = st.slider("Malzeme Kalınlığı (mm)", min_value=8, max_value=50, value=20)

# Sacın özellikleri
#sac_kalinlik = 20  # mm
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

# Dönme merkezini ayarla
x_pivot = torc_konum[0] + torc_genislik / 2  # Torcun orta noktası
y_pivot = torc_konum[1]-6 


# Işını çizme
beam_line, =plt.plot([torc_konum[0] + torc_genislik / 2, torc_konum[0] + torc_genislik / 2], [torc_konum[1] + torc_boyu, -isin_uzunluk], 'r--', label="Plazma Işını")


# Açıklamalar
plt.text(sac_uzunluk / 2, -5, f"Sac Kalınlığı: {sac_kalinlik} mm", ha='center', va='top')

angle_text = plt.text(0, 0, "", ha='right', va='bottom')
slope_text = plt.text(0, 0, "", ha='left', va='top')
slope_width_text = plt.text(0, 0, "", ha='center', va='bottom')  # Eğim genişliği için yeni metin

beam2_line, =plt.plot([torc_konum[1] + torc_boyu, -isin_uzunluk], [torc_konum[1] + torc_boyu, -isin_uzunluk], 'r--', label="Plazma Işını")
aci=-50

# 90 derece için eğim genişliği hesaplama
radyan_90 = np.radians(90)
m_90 = np.tan(radyan_90)
n_90 = torc_yukseklik + isin_uzunluk
kesisim_x_90 = (sac_kalinlik - n_90) / m_90
egim_genislik_90 = sac_uzunluk - kesisim_x_90

slope_width_line=None

# Grafikleri güncelleme fonksiyonu
def update_plot(aci):
        radyan = np.radians(aci)
        radyanisin = np.radians(aci+90)

        # Torcun dönme noktası (alt orta nokta)
        donme_noktasi_x = sac_uzunluk 
        donme_noktasi_y = torc_yukseklik - 6 

        # Torcun konumu (dönme noktasına göre hesaplanır)
        #torc_x = donme_noktasi_x - torc_genislik / 2 - torc_boyu * np.sin(radyan)
        #torc_y = donme_noktasi_y  * np.cos(radyan)
        #torc.set_xy((torc_x, torc_y))
        #torc.angle = aci  # Açıyı pozitif kullan
        tf = transforms.Affine2D().rotate_deg_around(x_pivot, y_pivot, aci)
        torc.set_transform(tf + ax.transData)

        # Işının uzunluğu (sacın altından 10 mm çıkacak şekilde)
        isin_uzunluk = sac_kalinlik + 100
        
        # Işını çizme (dönme noktasından başlar)
        beam_line.set_data(
            [donme_noktasi_x, donme_noktasi_x - isin_uzunluk * np.cos(radyanisin)],  # Işının x koordinatları
            [donme_noktasi_y, donme_noktasi_y - isin_uzunluk * np.sin(radyanisin)],  # Işının y koordinatları
        )


        # Işının denklemi: y = mx + n
        m = np.tan(radyanisin)  # Eğim
        n = donme_noktasi_y + sac_kalinlik  # Y-eksenini kestiği nokta

        # Işının sacla kesiştiği noktayı bulma
        kesisim_x = (sac_kalinlik - n) / m
        kesisim_y = sac_kalinlik

        # Eğim genişliğini hesaplama
        egim_genislik = sac_uzunluk - kesisim_x


        # Eğim genişliği çizgisi
        egim_cizgisi_x = [0, kesisim_x]  # Sacın sol kenarından kesişim noktasına kadar
        egim_cizgisi_y = [0, kesisim_y]  # Sacın alt kenarından kesişim noktasına kadar
        
        

        # Grafikleri güncelle
        """beam_line.set_data(
            [donme_noktasi_x, kesisim_x],  # Işının x koordinatları (kesişim noktasına kadar)
            [donme_noktasi_y, kesisim_y],  # Işının y koordinatları (kesişim noktasına kadar)
        )"""



        # Açıklamaları güncelle
        angle_text.set_text(f"Torç ({aci}°)")
        #angle_text.set_position((torc_x, torc_y))
        slope_text.set_text(f"Eğim ({aci:.1f}°)")
        slope_text.set_position((sac_uzunluk, sac_kalinlik))

            # Eğim genişliğini göster
        slope_width_text.set_text(f"Eğim Genişliği: {egim_genislik:.1f} mm")
        slope_width_text.set_position((sac_uzunluk / 2, sac_kalinlik / 2))  # Eğim genişliği metnini sacın ortasına yerleştir
        # Eğim genişliği farkını göster
        egim_farki = egim_genislik - egim_genislik_90
        beam2_line.set_data([donme_noktasi_x, donme_noktasi_x - egim_farki], [0, 0])
        beam2_line.set_color('yellow')
        slope_width_text.set_text(f"Eğim Farkı: {egim_farki:.1f} mm")
        slope_width_text.set_position((sac_uzunluk / 2, sac_kalinlik / 2))


        fig.canvas.draw_idle()




# İlk çizim
update_plot(gelenaci*-1)  # Başlangıçta progress bar değerini kullan


# Grafiği Streamlit uygulamasında göster
st.pyplot(fig)


