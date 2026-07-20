import streamlit as st
import pandas as pd

# 1. Sayfa Ayarları
st.set_page_config(page_title="GES Fizibilite & ROI", page_icon="☀️", layout="wide")

st.title("☀️ Güneş Enerjisi Fizibilite ve Amortisman Simülatörü")
st.markdown("**Yenilenebilir Enerji Yatırım ve Kapasite Planlama Aracı**")
st.write(
    "Bu araç, seçilen şehrin güneşlenme potansiyeline göre bir Güneş Enerjisi Santralinin (GES) üretim kapasitesini, finansal geri dönüşünü (ROI) ve çevresel etkisini hesaplar.")
st.divider()

# 2. Üç Sütunlu Kullanıcı Giriş Paneli
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("⚙️ Teknik Parametreler")
    # PyCharm uyarısını çözmek için float() ve int() ekledik
    panel_gucu = float(st.number_input("Birim Panel Gücü (W)", value=400, step=10))
    panel_sayisi = float(st.number_input("Panel Adedi", value=15, step=1, help="Kurulacak toplam panel sayısı."))
    verimlilik = float(st.slider("Sistem Performans Oranı (%)", 50, 100, 80))

with col2:
    st.subheader("📍 Konum ve Işınım")
    sehirler = {"İzmir": 5.2, "Antalya": 5.8, "Ankara": 4.8, "İstanbul": 4.2, "Bursa": 4.5}
    sehir = st.selectbox("Kurulum Bölgesi", list(sehirler.keys()))

    # Seçilen şehrin değeri float tipinde olmalı
    baz_guneslenme = float(sehirler[sehir] if sehir else 5.2)
    st.info(f"{sehir} için baz alınan ortalama günlük etkin güneşlenme: **{baz_guneslenme} saat**")

with col3:
    st.subheader("💰 Finansal Veriler")
    kurulum_maliyeti = float(st.number_input("Toplam Kurulum Maliyeti (TL)", value=150000, step=5000))
    elektrik_fiyati = float(st.number_input("Elektrik Birim Fiyatı (TL/kWh)", value=2.50, step=0.10))

# 3. Arka Plan Hesaplamaları
toplam_guc_kw = (panel_gucu * panel_sayisi) / 1000.0
gunluk_uretim_kwh = toplam_guc_kw * baz_guneslenme * (verimlilik / 100.0)
yillik_uretim_kwh = gunluk_uretim_kwh * 365.0

yillik_tasarruf = yillik_uretim_kwh * elektrik_fiyati
amortisman_yili = kurulum_maliyeti / yillik_tasarruf if yillik_tasarruf > 0 else 0.0

co2_tasarrufu_kg = yillik_uretim_kwh * 0.4
agac_esdegeri = co2_tasarrufu_kg / 22.0

st.divider()

# 4. Çıktı Gösterimi (Metrikler)
st.subheader("📊 Analiz Sonuçları")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Yıllık Enerji Üretimi", f"{yillik_uretim_kwh:,.0f} kWh")
m2.metric("Yıllık Finansal Getiri", f"{yillik_tasarruf:,.0f} ₺")
m3.metric("Amortisman (ROI) Süresi", f"{amortisman_yili:.1f} Yıl")
m4.metric("Engellenen CO2 (Ağaç)", f"~{co2_tasarrufu_kg / 1000:.1f} Ton ({int(agac_esdegeri)} 🌳)")

st.divider()

# 5. Veri Görselleştirme (Aylık Çubuk Grafik)
st.subheader("📈 Aylık Üretim Projeksiyonu")
st.write("Yaz aylarında artan ışınım değerlerine göre tahmini aylık üretim dağılımı.")

aylar = ["Oca", "Şub", "Mar", "Nis", "May", "Haz", "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]
dagilim_oranlari = [0.05, 0.06, 0.08, 0.10, 0.12, 0.13, 0.14, 0.12, 0.09, 0.06, 0.03, 0.02]
aylik_uretim_verisi = [float(yillik_uretim_kwh * oran) for oran in dagilim_oranlari]

chart_data = pd.DataFrame({"Aylar": aylar, "Üretim (kWh)": aylik_uretim_verisi})
st.bar_chart(chart_data.set_index("Aylar"), color="#a3e635")

st.success("Geliştirici: Efe Geylanioğlu | Enerji Sistemleri Mühendisliği")