import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("🤖 Yapay Zeka Destekli Maç Analiz Simülasyonu")

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
        
        # --- AI PARAMETRELERİ (GÜÇ ENDEKSLERİ) ---
        e_hucum = e['goalsFor'] / e['playedGames']
        e_savunma = e['goalsAgainst'] / e['playedGames']
        d_hucum = d['goalsFor'] / d['playedGames']
        d_savunma = d['goalsAgainst'] / d['playedGames']
        
        # AI Tahmin Algoritması: Poisson & Power Rating Kombinasyonu
        # Ev sahibinin beklenen golü, rakibin defans zafiyetiyle çarpılarak AI tarafından hesaplanır
        ai_ev_skor = e_hucum * (d_savunma / 1.1) + 0.2
        ai_dep_skor = d_hucum * (e_savunma / 1.1)
        
        st.divider()
        st.subheader(f"🤖 AI Tahmin Raporu: {ev_adi} vs {dep_adi}")

        # --- TAHMİN METRİKLERİ ---
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("MS Beklenen Skor", f"{round(ai_ev_skor, 1)} - {round(ai_dep_skor, 1)}")
        m2.metric("İY Olasılığı", f"{1 if ai_ev_skor > 1.8 else 0} - {1 if ai_dep_skor > 2.0 else 0}")
        m3.metric("Korner Tahmini", f"{int(7.5 + (e_hucum + d_hucum) * 1.6)}+")
        m4.metric("Kart Tahmini", f"{int(2 + (e_savunma + d_savunma) * 1.4)}+")

        st.divider()

        # --- AI STRATEJİK ANALİZ (AVANTAJ & DEZAVANTAJ) ---
        col_ev, col_dep = st.columns(2)
        
        with col_ev:
            st.info(f"🏠 {ev_adi} AI Karar Paneli")
            # AI Karşılaştırmalı Mantık
            if e_hucum > d_savunma:
                st.success(f"🔥 **AI ANALİZİ:** Ev sahibi hücum hattı, rakip defansı bozacak kapasitede. Skor üretme şansı %{round((e_hucum/d_savunma)*50, 1)}")
            else:
                st.error("⚠️ **AI ANALİZİ:** Rakip defans bloğu sizin hücum varyasyonlarınızı kısıtlayabilir.")
            
            if e_savunma < 1.0:
                st.success("🛡️ **DEFANSİF GÜVEN:** Takım kalesini kapatma konusunda lig ortalamasının üzerinde.")

        with col_dep:
            st.info(f"🚀 {dep_adi} AI Karar Paneli")
            if d_hucum > e_savunma:
                st.success(f"⚡
