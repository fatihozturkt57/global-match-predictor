import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Data Match Analiz", layout="wide")
st.title("⚽ Veri Tabanlı Karşılaştırmalı Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_yukle(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table'], res['competition']['name']
    except:
        return None, None

tablo, lig_adi = veri_yukle(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))
    
    # Lig Ortalamasını Hesapla (Takımları kıyaslamak için referans)
    lig_toplam_gol = sum(row['goalsFor'] for row in tablo)
    lig_toplam_mac = sum(row['playedGames'] for row in tablo)
    lig_ort_gol = lig_toplam_gol / lig_toplam_mac

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("📊 VERİLERİ ÇARPIŞTIR VE ANALİZ ET"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- ANALİZ MOTORU ---
        e_hucum = (e['goalsFor'] / e['playedGames']) / lig_ort_gol
        e_savunma = (e['goalsAgainst'] / e['playedGames']) / lig_ort_gol
        d_hucum = (d['goalsFor'] / d['playedGames']) / lig_ort_gol
        d_savunma = (d['goalsAgainst'] / d['playedGames']) / lig_ort_gol

        # Beklenen Goller (xG): Ev Sahibinin Hücumu * Deplasmanın Savunma Zayıflığı
        e_xg = e_hucum * d_savunma * lig_ort_gol * 1.10 # %10 Ev avantajı
        d_xg = d_hucum * e_savunma * lig_ort_gol

        st.divider()
        
        # --- SKOR VE İSTATİSTİK PANELİ ---
        st.subheader("🎯 Maç Dinamikleri ve Tahminler")
        m1, m2
