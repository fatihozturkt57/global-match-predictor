import streamlit as st
import requests
import random

# API Bilgileri
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz", layout="wide")
st.title("⚽ Profesyonel Maç Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    return requests.get(url, headers=HEADERS).json()['standings'][0]['table']

# --- ANA KOD BLOĞU BAŞLANGICI ---
try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev = st.selectbox("Ev Sahibi", takimlar)
    with c2: dep = st.selectbox("Deplasman", takimlar)

    if st.button("🔍 ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # İstatistik Hesaplama
        e_puan = round(e['points'] / e['playedGames'], 2)
        d_puan = round(d['points'] / d['playedGames'], 2)
        e_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        d_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        
        e_skor, d_skor = round(e_xg + 0.2), round(d_xg)

        st.divider()
        st.subheader("🎯 Tahmin ve Beklenen Skor")
        k1, k2, k3 = st.columns(3)
        k1.metric("Tahmini Skor", f"{e_skor} - {d_skor}")
        k2.write(f"🚩 Korner: {random.randint(9, 13)}+")
        k3.write(f"🟨 Kartlar: {random.randint(4, 7)}+")

        st.divider()
        st.subheader("🔬 Taktiksel Nedenler (Avantaj/Dezavantaj)")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev} Analizi")
            st.write(f"**Puan Ortalaması:** {e_puan}")
            if e_puan > 1.8:
                st.write("✅ **GÜÇLÜ YAN:** Takım ligin elit seviyesinde puan topluyor. Bu istikrar, zorlu anlarda oyun disiplinini kaybetmediklerini kanıtlıyor.")
            if e['goalsFor'] > e['goalsAgainst']:
                st.write("🔥 **HÜCUM ETKİSİ:** Attıkları gol yediklerinden fazla. Forvet hattı çok formda ve her an skoru değiştirebilecek kapasitede.")
            if e['goalsAgainst'] > 30:
                st.write("⚠️ **SAVUNMA ZAAFİYETİ:** Yenen toplam gol sayısı defans kurgusunda ciddi gedikler olduğunu gösteriyor, kontra ataklarda çok riskliler.")

        with a2:
            st.info(f"🚀 {dep} Analizi")
            st.
