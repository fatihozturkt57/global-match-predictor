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
        
        # --- GELİŞMİŞ VERİ ANALİZİ ---
        e_puan_ort = e['points'] / e['playedGames']
        d_puan_ort = d['points'] / d['playedGames']
        e_form = e.get('form', 'N/A').replace(',', ' ')
        d_form = d.get('form', 'N/A').replace(',', ' ')
        
        # Skor Tahmin Algoritması
        ev_gol_beklentisi = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        dep_gol_beklentisi = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        ev_skor = round(ev_gol_beklentisi + 0.4)
        dep_skor = round(dep_gol_beklentisi)

        st.divider()

        # 🚩 TAHMİN ÖZETİ
        st.subheader("🎯 Tahmin ve Beklenen Skor")
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            st.metric("Beklenen Skor", f"{ev_skor} - {dep_skor}")
        with k2:
            st.write(f"🚩 **Korner:** {random.randint(9, 13)}+")
        with k3:
            st.write(f"🟨 **Kart:** {random.randint(4, 7)}+")
        with k4:
            st.write(f"🌓 **İY Skoru:** {round(ev_skor/2)} - {round(dep_skor/2)}")

        st.divider()

        # 📊 DETAYLI KARŞILAŞTIRMA
        st.subheader("🔬 Taktiksel & Form Analizi")
        col_a, col_b = st.columns(2)

        with col_a:
            st.info(f"🏠 {ev} - Teknik Rapor")
            st.write(f"**Güncel Form:** {e_form}")
            st.write(f"**Puan Ortalaması:** {e_puan_ort:.2f}")
            
            st.markdown("---")
            if e_puan_ort > 2.0:
                st.write("✅ **Şampiyonluk Modu:** Takım şampiyonluk baskısını kaldırabiliyor.")
            if e['goalsFor'] > e['goalsAgainst']
