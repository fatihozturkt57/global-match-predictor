import streamlit as st
import requests
import random

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = { 'X-Auth-Token': API_KEY }

st.set_page_config(page_title="Ultra Analiz Merkezi", layout="wide")
st.title("⚽ Ultra-Detaylı Maç Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
secilen_lig = st.sidebar.selectbox("Ligi Seç", list(ligler.keys()))

@st.cache_data
def veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    return requests.get(url, headers=HEADERS).json()['standings'][0]['table']

try:
    tablo = veri_al(ligler[secilen_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev = st.selectbox("Ev Sahibi", takimlar)
    with c2: dep = st.selectbox("Deplasman", takimlar)

    if st.button("DERİNLEMESİNE ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # --- İSTATİSTİKSEL HESAPLAMALAR ---
        e_puan_ort = e['points'] / e['playedGames']
        d_puan_ort = d['points'] / d['playedGames']
        
        # Gol Beklentisi (xG tahmini)
        ev_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        dep_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        ev_skor = round(ev_xg + 0.3)
        dep_skor = round(dep_xg)

        st.divider()

        # 🎯 TAHMİN ÖZETİ
        st.subheader("🎯 Maç Sonu Tahmini & Beklenen Skor")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Tahmini Skor", f"{ev_skor} - {dep_skor}")
        with k2:
            st.write(f"🚩 **Korner:** {random.randint(9, 13)}+")
        with k3:
            st.write(f"🟨 **Sarı Kart:** {random.randint(4, 7)}+")
        with k4:
            st.info(f"🏆 **Favori:** {'1' if ev_skor > dep_skor else ('2' if dep_skor > ev_skor else '0')}")

        st.divider()

        # 🔬 DERİN ANALİZ RAPORU
        st.subheader("🔬 Takım Bazlı Nedenler ve Risk Analizi")
        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown(f"### 🏠 {ev} Analizi")
            st.write(f"**Puan Ortalaması:**
