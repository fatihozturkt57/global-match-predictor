import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("⚽ Yapay Zeka Destekli Maç Çarpıştırma Paneli")

# Ligler
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

    if st.button("🧠 AI ANALİZİ VE SİMÜLASYONU BAŞLAT"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- VERİ MADENCİLİĞİ (Data Mining) ---
        e_mac, d_mac = e['playedGames'], d['playedGames']
        e_hucum, e_defans = e['goalsFor'] / e_mac, e['goalsAgainst'] / e_mac
        d_hucum, d_defans = d['goalsFor'] / d_mac, d['goalsAgainst'] / d_mac
        
        # --- AI SKOR VE İSTATİSTİK MOTORU ---
        # Ev sahibi avantajı +0.2 eklenerek simüle edilir
        gol_ev = (e_hucum + d_defans) / 2 + 0.2
        gol_dep = (d_hucum + e_defans) / 2
        
        ms_e, ms_d = round(gol_ev), round(gol_dep)
        iy_e, iy_d = (1, 0) if gol_ev > 1.5 else (0, 0)
        if gol_dep > 1.8: iy_d = 1

        # Korner & Kart Algoritması (Baskı ve Sertlik Analizi)
        korner_skoru = round(7 + (e_hucum * 1.8) + (d_hucum * 1.2))
        kart_skoru = round(2 + (e_defans + d_defans) * 1.5)

        # --- EKRAN ÇIKTISI ---
        st.divider()
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📊 MS TAHMİNİ", f"{ms_e} - {ms_d}")
        col2.metric("🌓 İY TAHMİNİ", f"{iy_e} - {iy_d}")
        col3.metric("🚩 KORNER", f"{korner_skoru}+")
        col4.metric("🟨 KART", f"{kart_skoru}+")

        st.divider()
        
        # --- AVANTAJ / DEZAVANTAJ TABLOSU ---
        st.subheader("⚔️ Takım Kapışması: Avantaj & Dezavantaj")
