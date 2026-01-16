import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Match Expert", layout="wide")
st.title("🧠 AI Veri Madenciliği & Maç Simülasyonu")

# Lig Verisi Çekme
@st.cache_data
def get_league_data(code):
    url = f"https://api.football-data.org/v4/competitions/{code}/standings"
    try:
        r = requests.get(url, headers=HEADERS)
        return r.json()['standings'][0]['table']
    except Exception as e:
        return None

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Lig Seçin", list(ligler.keys()))
tablo = get_league_data(ligler[sec_lig])

if tablo:
    takim_listesi = {row['team']['name']: row for row in tablo}
    isimler = sorted(list(takim_listesi.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_sahibi = st.selectbox("Ev Sahibi", isimler)
    with c2: deplasman = st.selectbox("Deplasman", isimler)

    # BUTON VE ANALİZ BAŞLANGICI
    if st.button("🚀 AI ANALİZİ ÇALIŞTIR"):
        try:
            e = takim_listesi[ev_sahibi]
            d = takim_listesi[deplasman]
