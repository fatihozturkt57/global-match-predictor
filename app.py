import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("🤖 AI Destekli Profesyonel Analiz Simülasyonu")

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

    if st.button("🧠 AI ANALİZİNİ BAŞLAT"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        e_mac, d_mac = e['playedGames'], d['playedGames']
        
        if e_mac > 0 and d_mac > 0:
            # Temel Veriler
            e_hucum = e['goalsFor'] / e_mac
            e_savunma = e['goalsAgainst'] / e_mac
            d_hucum = d['goalsFor'] / d_mac
            d_savunma = d['goalsAgainst'] / d_mac
            
            # AI Skor Algoritması (xG üzerinden gerçek skor tahmini)
