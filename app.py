import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Match Engine v5", layout="wide")
st.title("🤖 AI Destekli Profesyonel Maç Simülatörü")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

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

    if st.button("🧠 AI ANALİZİ ÇALIŞTIR"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- AI MOTORU: GÜÇ PARAMETRELERİ ---
        e_hucum = e['goalsFor'] / e['playedGames']
        e_defans = e['goalsAgainst'] / e['playedGames']
        d_hucum = d['goalsFor'] / d['playedGames']
        d_defans = d['goalsAgainst'] / d['playedGames']
        
        # Avantaj Skorları (AI Mantığı)
        # Bir takımın hücumu, rakibin defansından ne kadar güçlü?
        e_ustunluk = e_hucum - d_defans
        d_ustunluk = d_hucum - e_defans
        
        # --- 1. TAHMİN MERKEZİ ---
        st.subheader("🎯 Yapay Zeka Skor Tahminleri")
        m1, m2, m3, m4 = st.columns(4)
        
        # Skor Simülasyonu
        skor_e = round(e_hucum * (d_defans / 1.2) + 0.3)
        skor_d = round(d_hucum * (e_defans / 1.2))
        
        m1.metric("Maç Sonu (MS)", f"{skor_e} - {skor_d}")
        m2.metric("İlk Yarı (İY)", f"{round(skor_e/2)} - {round(skor_d/2)}")
        
        # Korner ve Kart (Takımların agresiflik ve baskı verisinden)
        korner = round(8 + (e_hucum + d_hucum) * 1.5)
        kart = round(2 + (e_defans + d_defans) * 2)
        
        m3.metric("Tahmini Korner", f"{korner}+")
        m4.metric("Tahmini Kart", f"{kart}+")

        # --- 2. AVANTAJ / DEZAVANTAJ (KRİTİK ANALİZ) ---
        st.divider()
        st.subheader("⚖️ AI Çarpıştırma Raporu")
        a1, a2 = st.columns(2)
        
        with a1:
            st.markdown(f"### 🏠 {ev_adi}")
            if e_huc
