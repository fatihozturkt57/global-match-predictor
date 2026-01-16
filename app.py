import streamlit as st
import requests
import pandas as pd

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Data-Driven Pro Analiz", layout="wide")
st.title("⚽ Veri Madenciliği ve Karşılaştırmalı Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def lig_verilerini_getir(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table'], res['competition']['name']
    except:
        return None, None

tablo, lig_adi = lig_verilerini_getir(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))
    
    # Lig Geneli Ortalamalar (Güç Endeksi İçin)
    toplam_gol = sum(row['goalsFor'] for row in tablo)
    toplam_mac = sum(row['playedGames'] for row in tablo)
    lig_ort_gol = toplam_gol / toplam_mac

    col1, col2 = st.columns(2)
    with col1: ev_adi = st.selectbox("Ev Sahibi", takimlar)
    with col2: dep_adi = st.selectbox("Deplasman", takimlar)

    if st.button("📊 VERİ MADENCİLİĞİNİ BAŞLAT"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- GÜÇ ENDEKSİ HESAPLAMA (Power Ranking) ---
        # Bir takımın gol atma/yeme gücünün lig ortalamasına oranı
        e_hucum_endeks = (e['goalsFor'] / e['playedGames']) / lig_ort_gol
        e_savunma_endeks = (e['goalsAgainst'] / e['playedGames']) / lig_ort_gol
        d_hucum_endeks = (d['goalsFor'] / d['playedGames']) / lig_ort_gol
        d_savunma_endeks = (d['goalsAgainst'] / d['playedGames']) / lig_ort_gol

        # Beklenen Goller (xG) - Takımların güçlerinin çapraz çarpımı
        # Ev sahibi avantajı için global standart olan %15 (1.15) çarpanı eklenmiştir
        e_xg = e_hucum_endeks * d_savunma_endeks * lig_ort_gol * 1.15
        d_xg = d_hucum_endeks * e_savunma_endeks * lig_ort_gol

        st.divider()
        
        # --- ANALİZ RAPORU ---
        st.subheader(f"🔍 {ev_adi} - {dep_adi} Veri Karşılaştırması")
        
        res1, res2 = st.columns(2)
        with res1:
            st.info(f"🏠 {ev_adi} Analizi")
            st.write(f"**Hücum Verimliliği:** %{round(e_hucum_endeks * 100)}")
            st.write(f"**Savunma Direnci:** %{round((2 - e_savunma_endeks) * 100)}") # 1.0 altı iyidir
            if e_hucum_endeks > 1.3: st.success("✅ Rakip defansın arkasına sarkma kapasitesi çok yüksek.")
            if e_savunma_endeks > 1.2: st.error("❌ Kendi yarı sahasında ciddi boşluklar veriyor.")

        with res2:
            st.info(f"🚀 {dep_adi} Analizi")
            st.write(f"**Hücum Verimliliği:** %{round(d_hucum_endeks * 100)}")
            st.write(f"**Savunma Direnci:** %{round((2 - d_savunma_endeks) * 100)}")
            if d_hucum_endeks > e_hucum_endeks: st.warning("⚠️ Deplasman takımı gol yollarında ev sahibinden daha keskin.")
            if d_savunma_endeks < 0.9: st.success("🛡️ Kapalı savunma kurgusuyla geçit vermeyebilir.")

        # --- DİNAMİK TAHMİN MERKEZİ ---
        st.divider()
        st.subheader("🎯 İstatistiksel Tahminler")
        
        m1, m2, m3, m4 = st.columns(4)
        
        # Skor Tahmini (xG üzerinden daha hassas)
        m1.metric("Beklenen Skor (MS)", f"{round(e_xg
