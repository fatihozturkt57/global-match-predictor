import streamlit as st
import requests
import random

# API Bilgileri
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Ultra Analiz Paneli", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
secilen_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    return res['standings'][0]['table']

try:
    tablo = veri_al(ligler[secilen_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🚀 DERİNLEMESİNE ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # Matematiksel Model
        e_puan = e['points'] / e['playedGames']
        d_puan = d['points'] / d['playedGames']
        ev_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        dep_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        ev_skor = round(ev_xg + 0.3)
        dep_skor = round(dep_xg)

        st.divider()

        # 1. BÖLÜM: ANA TAHMİNLER
        st.subheader("🎯 Maç Sonu & Skor Beklentisi")
        k1, k2, k3, k4 = st.columns(4)
        with k1: st.metric("Beklenen Skor", f"{ev_skor} - {dep_skor}")
        with k2: st.write(f"🚩 Korner: {random.randint(9, 13)}+")
        with k3: st.write(f"🟨 Kartlar: {random.randint(4, 7)}+")
        with k4: st.write(f"🌓 İY Skoru: {round(ev_skor/2)} - {round(dep_skor/2)}")

        st.divider()

        # 2. BÖLÜM: AVANTAJ / DEZAVANTAJ (DETAYLI)
        st.subheader("🔬 Taktiksel Nedenler")
        col_a, col_b = st.columns(2)

        with col_a:
            st.info(f"🏠 {ev} Analiz")
            st.write(f
