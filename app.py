import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz Paneli v2", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Sistemi")

ligler = {
    "İngiltere": "PL", 
    "İspanya": "PD", 
    "İtalya": "SA", 
    "Almanya": "BL1", 
    "Fransa": "FL1"
}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    response = requests.get(url, headers=HEADERS)
    return response.json()['standings'][0]['table']

try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col1, col2 = st.columns(2)
    with col1: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with col2: dep = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 GERÇEK VERİYLE ANALİZ ET"):
        e, d = veriler[ev], veriler[dep]
        
        # --- VERİ ANALİZİ ---
        e_mac = e['playedGames']
        d_mac = d['playedGames']
        
        # 1. Gol Beklentisi (xG) Hesabı
        e_hucum = e['goalsFor'] / e_mac
        e_savunma = e['goalsAgainst'] / e_mac
        d_hucum = d['goalsFor'] / d_mac
        d_savunma = d['goalsAgainst'] / d_mac
        
        # Ev sahibi avantajı (+0.3) ve çapraz eşleşme
        e_skor_tahmin = (e_hucum + d_savunma) / 2 + 0.3
        d_skor_tahmin = (d_hucum + e_savunma) / 2
        
        # 2. Dinamik Korner Tahmini (Hücum gücü arttıkça korner artar)
        # Toplam gol beklentisi üzerinden bir katsayı (Hücumcu takımlar = daha çok korner)
        korner_baz = 7.5
        korner_tahmin = korner_baz + (e_hucum + d_hucum) * 1.2
        
        # 3. Dinamik Kart Tahmini (Savunma zayıflığı ve rekabet)
        # Savunması kötü takımlar daha çok faul yapar / Maç çekişmeliyse kart artar
        kart_baz = 2.5
        kart_tahmin = kart_baz + (e_savunma + d_savunma) * 0.8
        
        # 4. İY Skoru (Genelde maçın ilk yarısında toplam golün %40'ı atılır)
        iy_e = round(e_skor_tahmin * 0.45)
        iy_d = round(d_skor_tahmin * 0.40)

        # --- GÖRSELLEŞTİRME ---
        st.divider()
        st.subheader("🎯 Takım Verilerine Dayalı Tahminler")
        k1, k2, k3, k4 = st.columns(4)
        
        k1.metric("Beklenen Skor", f"{round(e_skor_tahmin)}-{round(d_skor_tahmin)}")
        k2.metric("Tahmini Korner", f"{round(korner_tahmin, 1)}+")
        k3.metric("Tahmini Kart", f"{round(kart_tahmin, 1)}+")
        k4.metric("İlk Yarı Skoru", f"{iy_e}-{iy_d}")

        st.divider()
        # Dinamik Analiz Notları
        st.subheader("🔬 Taktiksel Veri Analizi")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev}")
            st.write(f"**Maç Başı Gol:** {round(e_hucum, 2)}")
            if e_hucum > 2.0: st.success("🔥 Olağanüstü hücum hattı.")
            if e_savunma < 1.0: st.success("🛡️ Defans bloğu çok sağlam.")
            else: st.warning("⚠️ Savunmada boşluklar veriyor.")

        with a2:
            st.info(f"🚀 {dep}")
            st.write(f"**Maç Başı Gol:** {round(d_hucum, 2)}")
            if d_hucum > e_hucum: st.warning("⚡ Deplasman takımı gol yollarında daha üretken.")
            if d['lost'] < 5: st.success("📈 Yenilmesi zor bir takım.")
            else: st.error("📉 Kaybetme alışkanlığı oluşmuş.")

except Exception as e:
    st.error(f"Bir hata oluştu veya API limiti doldu. Lütfen tekrar deneyin. Hata: {e}")
