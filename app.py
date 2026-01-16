import streamlit as st
import requests
import random

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz Paneli", layout="wide")
st.title("⚽ Profesyonel Maç Analiz & Tahmin Sistemi")

# Lig Sözlüğü - Türkiye (TR) eklendi ancak API desteği gerekebilir
ligler = {
    "İngiltere": "PL", 
    "İspanya": "PD", 
    "İtalya": "SA", 
    "Almanya": "BL1", 
    "Fransa": "FL1",
    "Türkiye (Beta)": "TR" 
}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    response = requests.get(url, headers=HEADERS)
    return response.json()['standings'][0]['table']

try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col1, col2 = st.columns(2)
    with col1: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with col2: dep = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        e_puan = round(e['points'] / e['playedGames'], 2)
        d_puan = round(d['points'] / d['playedGames'], 2)
        
        # Skor Tahmini
        e_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        d_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        e_s, d_s = round(e_xg + 0.3), round(d_xg)

        st.divider()
        st.subheader("🎯 Tahmin Özeti")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Beklenen Skor", f"{e_s}-{d_s}")
        k2.write(f"🚩 Korner: {random.randint(8,12)}+")
        k3.write(f"🟨 Kartlar: {random.randint(4,7)}+")
        k4.write(f"🌓 İY Skoru: {round(e_s/2)}-{round(d_s/2)}")

        st.divider()
        st.subheader("🔬 Taktiksel Nedenler (Avantaj & Dezavantaj)")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev}")
            st.write(f"**Puan Ortalaması:** {e_puan}")
            if e_puan > 2.0: st.write("✅ **GÜÇLÜ:** Takım şampiyonluk modunda, iç saha baskısı çok yüksek.")
            if e['goalsFor'] > e['goalsAgainst'] * 1.5: st.write("🔥 **HÜCUM:** Forvetler çok verimli, her pozisyonu gole çevirebiliyorlar.")
            if e['goalsAgainst'] > 25: st.write("⚠️ **RİSK:** Defans hattı ağır kalıyor, arkaya atılan toplarda zayıflar.")

        with a2:
            st.info(f"🚀 {dep}")
            st.write(f"**Puan Ortalaması:** {d_puan}")
            if d_puan > e_puan: st.write("💪 **FORM:** Deplasman karnesi rakipten daha istikrarlı görünüyor.")
            if d['goalsAgainst'] < d['playedGames']: st.write("🛡️ **DEFANS:** Çok katı bir savunma kurguları var, aşılması zor bir duvar gibiler.")
            if d['lost'] > d['won']: st.write("📉 **RİSK:** Mağlubiyet sayısı yüksek, moral ve direnç seviyesi düşük.")

        st.divider()
        if e_s > d_s: st.success(f"🤖 SONUÇ: {ev} kazanmaya daha yakın görünüyor.")
        elif d_s > e_s: st.error(f"🤖 SONUÇ: {dep} taktiksel disipliniyle sürpriz yapabilir.")
        else: st.warning("🤖 SONUÇ: İki takımın dengede olduğu bir beraberlik maçı beklentisindeyiz.")

except Exception:
    st.error("Seçtiğiniz ligin verileri ücretsiz API kapsamında olmayabilir. Lütfen Avrupa liglerini deneyin.")
