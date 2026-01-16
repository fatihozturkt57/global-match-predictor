import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Match Predictor", layout="wide")
st.title("🧠 Yapay Zeka Destekli Stratejik Analiz")

# Lig Seçimi
ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def lig_verisi_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data['standings'][0]['table']
    except:
        return None

tablo = lig_verisi_cek(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🧠 AI SİMÜLASYONUNU BAŞLAT"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- VERİ MADENCİLİĞİ ---
        e_m, d_m = e['playedGames'], d['playedGames']
        e_hucum = e['goalsFor'] / e_m
        e_defans = e['goalsAgainst'] / e_m
        d_hucum = d['goalsFor'] / d_m
        d_defans = d['goalsAgainst'] / d_m
