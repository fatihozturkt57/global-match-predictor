import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Match Sim", layout="wide")
st.title("⚽ AI Stratejik Maç Karşılaştırma Motoru")

# Ligler
ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Analiz Edilecek Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table']
    except:
        return None

tablo = veri_cek(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    # ANALİZ TETİKLEYİCİ BUTON
    if st.button("🧠 AI ANALİZİ VE SİMÜLASYONU BAŞLAT"):
        e = veriler[ev_adi]
        d = veriler[dep_adi]
        
        # 1. VERİ İŞLEME (AI Girdileri)
        e_m, d_m = e['playedGames'], d['playedGames']
        
        if e_m > 0 and d_m > 0:
            e_h = e['goalsFor'] / e_m
            e_d = e['goalsAgainst'] / e_m
            d_h = d['goalsFor'] / d_m
            d_d = d['goalsAgainst'] / d_m

            # 2. AI SİMÜLASYON MOTORU (Olasılık Hesaplama)
            # Ev sahibinin gücü rakip defans zayıflığıyla çarpıştırılır
            ev_beklenen = (e_h * d_d) ** 0.5 + 0.3
            dep_beklenen = (d_h * e_d) ** 0.5
            
            # Galibiyet Olasılığı
            toplam_guc = ev_beklenen + dep_beklenen
            ev_olasil
