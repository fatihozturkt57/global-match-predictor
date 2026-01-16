import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz", layout="wide")
st.title("⚽ Profesyonel Maç Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_yukle(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table']
    except:
        return None

tablo = veri_yukle(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("📊 ANALİZİ BAŞLAT"):
        e = veriler[ev_adi]
        d = veriler[dep_adi]
        
        # Verileri Hesaplama
        e_m, d_m = e['playedGames'], d['playedGames']
        
        if e_m > 0 and d_m > 0:
            e_at = e['goalsFor'] / e_m
            e_ye = e['goalsAgainst'] / e_m
            d_at = d['goalsFor'] / d_m
            d_ye = d['goalsAgainst'] / d_m

            # xG Hesaplama
