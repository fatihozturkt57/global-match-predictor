import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz v6", layout="wide")
st.title("⚽ Veri Odaklı Karşılaştırmalı Analiz")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table']
    except Exception as e:
        return None

tablo = veri_al(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("📊 ANALİZİ ÇALIŞTIR"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- MATEMATİKSEL ANALİZ MOTORU ---
        e_mac, d_mac = e['playedGames'], d['playedGames']
        
        # Takım Güç Endeksleri (Maç Başı Ortalama)
        e_atilan = e['goalsFor'] / e_mac
        e_yenilen = e['goalsAgainst'] / e
