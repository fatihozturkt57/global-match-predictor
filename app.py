import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz v7", layout="wide")
st.title("⚽ Profesyonel Maç Çarpıştırma & Analiz")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_getir(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        # API'den gelen verinin doğruluğunu kontrol et
        if 'standings' in res:
            return res['standings'][0]['table']
        return None
    except:
        return None

tablo = veri_getir(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("📊 GERÇEK VERİLERİ ANALİZ ET"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- DOĞRU HESAPLAMA MANTIĞI ---
        # Sayıyı sözlüğe değil, sözlüğün içindeki 'playedGames' değerine bölüyoruz
        e_mac, d_mac = e['playedGames'], d['playedGames']
        
        e_atilan_ort = e['goalsFor'] / e_mac
        e_yenilen_ort = e['goalsAgainst'] / e_mac
        d_atilan_ort = d['goalsFor'] / d_mac
        d_yenilen_ort = d['goalsAgainst'] / d_mac

        # Karşılıklı Güç Analizi (xG Simülasyonu)
        # Ev sahibi skoru = (Ev hücum gücü + Deplasman defans zaafı
