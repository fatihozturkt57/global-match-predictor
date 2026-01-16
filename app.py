import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz", layout="wide")
st.title("📊 Gerçek Veri Karşılaştırma Paneli")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_getir(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    return res['standings'][0]['table']

# Veriyi çek ve doğrula
try:
    tablo = veri_getir(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 ANALİZİ BAŞLAT"):
        # Takım verilerini al
        e = veriler[ev_adi]
        d = veriler[dep_adi]
        
        # Maç sayıları
        e_m, d_m = e['playedGames'], d['playedGames']
        
        # --- ANALİZ MANTIĞI (Her takıma göre değişen sonuçlar) ---
        # 1. Maç başı gol ortalamaları
        e_at = e['goalsFor'] / e_m
        e_ye = e['goalsAgainst'] / e_m
        d_at = d['goalsFor'] / d_m
        d_ye = d['goalsAgainst'] / d_m

        # 2. Karşılıklı Skor Tahmini (xG Mantığı)
        # Evin atacağı: (Kendi hücumu + Rakip defans zafiyeti) / 2
        e_tahmin = (e_at + d_ye) / 2 + 0.2
        d_tahmin = (d_at + e_ye) / 2

        # --- EKRANA YAZDIRMA ---
        st.divider()
        st.subheader(f"🏟️ {
