import streamlit as st
import requests
import random

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Analiz Paneli", layout="wide")
st.title("⚽ Profesyonel Maç Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    return requests.get(url, headers=HEADERS).json()['standings'][0]['table']

try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    ev = st.selectbox("Ev Sahibi", takimlar)
    dep = st.selectbox("Deplasman", takimlar)

    if st.button("🔍 ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        e_puan = round(e['points'] / e['playedGames'], 2)
        d_puan = round(d['points'] / d['playedGames'], 2)
        
        # Skor Hesaplama
        e_xg = (e['goalsFor'] / e['playedGames'] + d['goalsAgainst'] / d['playedGames']) / 2
        d_xg = (d['goalsFor'] / d['playedGames'] + e['goalsAgainst'] / e['playedGames']) / 2
        e_s, d_s = round(e_xg + 0.2), round(d_xg)

        st.divider()
        st.subheader("🎯 Tahmin Raporu")
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Skor Tahmini", f"{e_s}-{d_s}")
        k2.write(f"🚩 Korner: {random.randint(8,12)}+")
        k3.write(f"🟨 Kart: {random.randint(3,6)}+")
        k4.write(f"🌓 İY: {round(e_s/2)}-{round(d_s/2)}")

        st.divider()
        st.subheader("🔬 Taktiksel Nedenler")
        a1, a2 = st.columns(2)

        with a1:
            st.info(f"🏠 {ev}")
            st.write(f"**Puan Ort:** {e_puan}")
            if e_puan > 1.8: st.write("✅ **GÜÇLÜ:** Takım elit seviyede, istikrarı çok yüksek.")
            if e['goalsFor'] > 35: st.write("🔥 **HÜCUM:** Gol yollarında ligin en etkili ekiplerinden.")
            if e['goalsAgainst'] > 25: st.write("⚠️ **RİSK:** Defansı kolay aşılıyor, kontra riskli.")

        with a2:
            st.info(f"🚀 {dep}")
            st.write(f"**Puan Ort:** {d_puan}")
            if d_puan > e_puan: st.write("✅ **GÜÇLÜ:** Deplasmanda olmasına rağmen daha formda.")
            if d['goalsAgainst'] < 20: st.write("🛡️ **DEFANS:** Ligin en katı savunmalarından birine sahip.")
            if d['lost'] > 8: st.write("📉 **RİSK:** Mağlubiyet alışkanlığı var, direnci düşük.")

        st.divider()
        if e_s > d_s: st.success(f"🤖 SONUÇ: {ev} kazanır. Saha avantajı ve kadro gücü önde.")
        elif d_s > e_s: st.error(f"🤖 SONUÇ: {dep} kazanır. Taktik disiplini galibiyeti getirir.")
        else: st.warning("🤖 SONUÇ: Maç berabere biter. İki takımın güçleri birbirine çok yakın.")

except Exception:
    st.error("Bir hata oluştu. Lütfen sayfayı yenileyip tekrar deneyin.")
