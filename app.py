import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("🧠 AI Veri Madenciliği & Stratejik Analiz")

@st.cache_data
def lig_verisi_al(code):
    url = f"https://api.football-data.org/v4/competitions/{code}/standings"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        return r.json()['standings'][0]['table']
    except Exception as e:
        st.error(f"API Hatası: {e}")
        return None

ligler = {
    "İngiltere": "PL",
    "İspanya": "PD",
    "İtalya": "SA",
    "Almanya": "BL1",
    "Fransa": "FL1"
}

sec_lig = st.sidebar.selectbox("Lig Seçin", list(ligler.keys()))
tablo = lig_verisi_al(ligler[sec_lig])

if tablo:
    takimlar_db = {row['team']['name']: row for row in tablo}
    isimler = sorted(takimlar_db.keys())

    c1, c2 = st.columns(2)
    with c1:
        ev_adi = st.selectbox("Ev Sahibi", isimler)
    with c2:
        dep_adi = st.selectbox("Deplasman", isimler)

    if st.button("🚀 AI ANALİZİ BAŞLAT"):
        try:
            e = takimlar_db[ev_adi_]()_
