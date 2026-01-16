import streamlit as st
import requests
import random

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = { 'X-Auth-Token': API_KEY }

st.set_page_config(page_title="Süper Analiz Paneli", layout="wide")
st.title("🛡️ Profesyonel Futbol Analiz & Tahmin Merkezi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
secilen_lig = st.sidebar.selectbox("Ligi Seç", list(ligler.keys()))

@st.cache_data
def veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    return requests.get(url, headers=HEADERS).json()['standings'][0]['table']

try:
    tablo = veri_al(ligler[secilen_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col_e, col_d = st.columns(2)
    with col_e: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with col_d: dep = st.selectbox("Deplasman Takım", takimlar)

    if st.button("🔍 DEV ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # --- İSTATİSTİKSEL HESAPLAMALAR ---
        e_gucu = e['goalsFor'] / e['playedGames']
        d_gucu = d['goalsFor'] / d['playedGames']
        e_defans = e['goalsAgainst'] / e['playedGames']
        d_defans = d['goalsAgainst'] / d['playedGames']
        
        # Skor Tahmini
        ev_skor = round((e_gucu + d_defans) / 2 + 0.3) # +0.3 ev sahibi avantajı
        dep_skor = round((d_gucu + e_defans) / 2)
        
        st.divider()

        # 1. BÖLÜM: TAHMİN ÖZETİ (KİM KAZANIR?)
        st.subheader("🏆 Maç Sonu & Skor Tahmini")
        c1, c2, c3 = st.columns(3)
        with c1:
            if ev_skor > dep_skor: st.success(f"**MAÇ SONUCU: 1**\n\n({ev} Favori)")
            elif dep_skor > ev_skor: st.error(f"**MAÇ SONUCU: 2**\n\n({dep} Favori)")
            else: st.warning("**MAÇ SONUCU: 0**\n\n(Beraberlik)")
        with c2:
            st.metric("Tahmini Skor", f"{ev_skor} - {dep_skor}")
            st.write(f"İY Skoru: {round(ev_skor/2)} - {round(dep_skor/2)}")
        with c3:
            st.write(f"🚩
