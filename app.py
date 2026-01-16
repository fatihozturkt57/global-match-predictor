import streamlit as st
import requests
import random

# API Yapılandırması
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz Sistemi", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Merkezi")

lig_sozluk = {
    "İngiltere": "PL",
    "İspanya": "PD",
    "İtalya": "SA",
    "Almanya": "BL1",
    "Fransa": "FL1"
}

secilen_lig_ad = st.sidebar.selectbox("Ligi Seçin", list(lig_sozluk.keys()))
lig_kodu = lig_sozluk[secilen_lig_ad]

@st.cache_data
def verileri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    return res['standings'][0]['table']

try:
    puan_durumu = verileri_cek(lig_kodu)
    takim_verileri = {row['team']['name']: row for row in puan_durumu}
    liste = sorted(list(takim_verileri.keys()))

    sol_kol, sag_kol = st.columns(2)
    with sol_kol:
        ev_takim = st.selectbox("Ev Sahibi Takım", liste)
    with sag_kol:
        dep_takim = st.selectbox("Deplasman Takımı", liste)

    if st.button("🔍 ANALİZİ BAŞLAT"):
        e = takim_verileri[ev_takim]
        d = takim_verileri[dep_takim]
        
        # Temel İstatistikler
        e_puan = round(e['points'] / e['playedGames'], 2)
        d_puan = round(d['points'] / d['playedGames'], 2)
        
        # Skor Tahmini (xG Mantığı)
        e_gol_beklenti = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        d_gol_beklenti = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        e_skor = round(e_gol_beklenti + 0.3)
        d_skor = round(d_gol_beklenti)

        st.divider()

        # 1. BÖLÜM: SKOR VE İSTATİSTİK
        st.subheader("🎯 Tahmin Raporu")
        m1, m2, m3 = st.columns(3)
        m1.metric("Beklenen Skor", f"{e_skor} - {d_skor}")
        m2.write(f"🚩 Korner: {random.randint(9, 13)}+")
        m3.write(f"🟨 Kart: {random.randint(4, 7)}+")

        st.divider()

        # 2. BÖLÜM: AVANTAJ / DEZAVANTAJ
        st.subheader("🔬 Taktiksel Analiz")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev_takim} Analizi")
            st.write(f"Puan Ortalaması: {e_puan}")
            if e_puan > 1.8:
                st.write("✅ **Avantaj:** Takım şampiyonluk formunda ve çok istikrarlı.")
            if e['goalsFor'] > e['goalsAgainst']:
                st.write("✅ **Avantaj:** Hücum hattı, savunma hatalarını telafi edebilecek güçte.")
            if (
