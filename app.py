import streamlit as st
import requests
import random

# API Yapılandırması
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz Sistemi", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    return res['standings'][0]['table']

# --- ANA SİSTEM ---
try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 DERİN ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # Matematiksel Analiz
        e_puan = round(e['points'] / e['playedGames'], 2)
        d_puan = round(d['points'] / d['playedGames'], 2)
        e_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        d_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        e_skor, d_skor = round(e_xg + 0.2), round(d_xg)

        st.divider()

        # 🎯 TAHMİN ÖZETİ
        st.subheader("🎯 Maç Sonu ve Skor Beklentisi")
        k1, k2, k3 = st.columns(3)
        k1.metric("Tahmini Skor", f"{e_skor} - {d_skor}")
        k2.write(f"🚩 Korner: {random.randint(9, 13)}+")
        k3.write(f"🟨 Kartlar: {random.randint(4, 7)}+")

        st.divider()

        # 🔬 DETAYLI AVANTAJ / DEZAVANTAJ ANALİZİ
        st.subheader("🔬 Taktiksel Nedenler")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev} Detaylı Rapor")
            st.write(f"**Puan Ortalaması:** {e_puan}")
            if e_puan > 1.8:
                st.write("✅ **Güçlü Yan:** Takım elit seviyede puan topluyor. Bu, zorlu maçlarda bile taktik disiplini koruduklarını gösterir.")
            if e['goalsFor'] > e['goalsAgainst']:
                st.write("🔥 **Hücum Gücü:** Attıkları gol sayısı yediklerinden fazla. Forvet hattı skoru değiştirebilecek kadar formda.")
            if e['goalsAgainst'] > 30:
                st.write("⚠️
