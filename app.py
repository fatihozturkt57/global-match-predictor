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
        r = requests.get(url, headers=HEADERS)
        return r.json()['standings'][0]['table']
    except:
        return None

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Lig Seçin", list(ligler.keys()))
tablo = lig_verisi_al(ligler[sec_lig])

if tablo:
    takimlar_db = {row['team']['name']: row for row in tablo}
    isimler = sorted(list(takimlar_db.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi", isimler)
    with c2: dep_adi = st.selectbox("Deplasman", isimler)

    if st.button("🚀 AI ANALİZİ BAŞLAT"):
        # Veri çekme ve hesaplama kısmı (Try-Except içinde)
        try:
            e = takimlar_db[ev_adi]
            d = takimlar_db[dep_adi]
            
            e_mac = max(e['playedGames'], 1)
            d_mac = max(d['playedGames'], 1)
            
            # AI Parametreleri: Hücum/Savunma Katsayıları
            e_h = e['goalsFor'] / e_mac
            e_s = e['goalsAgainst'] / e_mac
            d_h = d['goalsFor'] / d_mac
            d_s = d['goalsAgainst'] / d_mac

            # AI Simülasyonu (XG ve Olasılık Modeli)
            ev_xg = (e_h * d_s) ** 0.5 + 0.25
            dep_xg = (d_h * e_s) ** 0.5
            
            # Galibiyet Yüzdesi Hesaplama
            toplam_guc = ev_xg + dep_xg
            ev_win_rate = round((ev_xg / toplam_xg if (toplam_xg := ev_xg + dep_xg) > 0 else 0.5) * 100)

            # --- GÖRSEL SONUÇLAR ---
            st.divider()
            st.header(f"📊 {ev_adi} - {dep_adi} AI Raporu")
            
            m1, m
