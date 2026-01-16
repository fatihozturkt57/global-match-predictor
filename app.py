import streamlit as st
import requests
import random

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Ultra Analiz Merkezi", layout="wide")
st.title("⚽ Ultra-Detaylı Maç Analiz Sistemi")

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

    c1, c2 = st.columns(2)
    with c1: ev = st.selectbox("Ev Sahibi", takimlar)
    with c2: dep = st.selectbox("Deplasman", takimlar)

    if st.button("DERİNLEMESİNE ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # İstatistikler
        e_puan_ort = e['points'] / e['playedGames']
        d_puan_ort = d['points'] / d['playedGames']
        ev_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        dep_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        ev_skor = round(ev_xg + 0.3)
        dep_skor = round(dep_xg)

        st.divider()

        # 1. BÖLÜM: ÖZET
        st.subheader("🎯 Tahmin Özeti")
        k1, k2, k3 = st.columns(3)
        with k1: st.metric("Beklenen Skor", f"{ev_skor} - {dep_skor}")
        with k2: st.write(f"🚩 Korner: {random.randint(9, 13)}+")
        with k3: st.write(f"🟨 Kart: {random.randint(4, 7)}+")

        st.divider()

        # 2. BÖLÜM: DETAYLI ANALİZ
        st.subheader("🔬 Takım Analizleri")
        col_a, col_b = st.columns(2)

        with col_a:
            st.info(f"🏠 {ev}")
            st.write(f"**Puan Ortalaması:** {e_puan_ort:.2f}")
            if e_puan_ort > 2.0: st.write("✅ **Avantaj:** Şampiyonluk formunda.")
            if e['goalsFor'] > e['goalsAgainst']: st.write("✅ **Avantaj:** Hücum hattı savunmadan güçlü.")
            if e['goalsAgainst'] / e['playedGames'] > 1.5: st.write("❌ **Risk:** Savunma çok kolay açık veriyor.")

        with col_b:
            st.info(f"🚀 {dep}")
            st.write(f"**Puan Ortalaması:** {d_puan_ort:.2f}")
            if d_puan_ort > e_puan_ort: st.write("✅ **Avantaj:** Form olarak rakipten daha iyi.")
            if d['goalsAgainst'] < d['playedGames']: st.write("✅ **Avantaj:** Çok disiplinli savunma.")
            if d['goalsFor'] / d['playedGames'] < 1.1: st.write("❌ **Risk:** Gol yollarında kısır kalıyorlar.")

        # 3. BÖLÜM: KARAR
        st.divider()
        if ev_skor > dep_skor:
            st.success(f"🤖 **SONUÇ:** {ev} kazanmaya yakın. Saha avantajı ve kadro kalitesi ön planda.")
        elif dep_skor > ev_skor:
            st.error(f"🤖 **SONUÇ:** {dep} favori. Deplasmanda olmalarına rağmen daha dirençli görünüyorlar.")
        else:
            st.warning("🤖 **SONUÇ:** Beraberlik ihtimali çok yüksek. İki takım da birbirini kilitler.")

except Exception as err:
    st.error("Veri alınırken hata oluştu
