import streamlit as st
import requests

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = { 'X-Auth-Token': API_KEY }

st.set_page_config(page_title="Pro Analiz Sistemi", layout="wide")
st.title("🛡️ Stratejik Maç Analiz Raporu")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
secilen_lig = st.sidebar.selectbox("Ligi Seç", list(ligler.keys()))

@st.cache_data
def detayli_veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    return requests.get(url, headers=HEADERS).json()['standings'][0]['table']

try:
    tablo = detayli_veri_al(ligler[secilen_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col1, col2 = st.columns(2)
    with col1: ev = st.selectbox("Ev Sahibi", takimlar)
    with col2: dep = st.selectbox("Deplasman", takimlar)

    if st.button("DETAYLI ANALİZİ GÖSTER"):
        e, d = veriler[ev], veriler[dep]
        
        st.markdown(f"### 📋 {ev} vs {dep} Maç Raporu")
        
        col_ev, col_dep = st.columns(2)
        
        with col_ev:
            st.info(f"🏠 **{ev} Neden Kazanabilir? (Avantajlar)**")
            if e['points'] > d['points']:
                st.write("- **Puan Üstünlüğü:** Genel tabloda daha istikrarlı bir grafik çiziyorlar.")
            if (e['goalsFor'] / e['playedGames']) > 1.8:
                st.write("- **Hücum Hattı Formda:** Takım maç başına yüksek gol ortalamasıyla oynuyor; bitiricilikleri yüksek.")
            st.write("- **Ev Sahibi Psikolojisi:** Seyirci desteği ve saha alışkanlığı bu seviyedeki maçlarda taktik disiplini artırır.")

            st.error(f"⚠️ **{ev} Neden Kaybedebilir? (Dezavantajlar)**")
            if e['goalsAgainst'] > 30:
                st.write("- **Savunma Zafiyeti:** Takım arkada çok boşluk veriyor, kontra ataklarda zorlanabilirler.")
            if e['playedGames'] > 20 and (e['goalsFor'] < 25):
                st.write("- **Üretkenlik Sorunu:** Forvet hattı son haftalarda gol yollarında etkisiz kalıyor, bitiricilik zayıf.")

        with col_dep:
            st.success(f"🚀 **{dep} Neden Kazanabilir? (Avantajlar)**")
            if d['points'] > e['points']:
                st.write("- **Kadro Kalitesi:** Puan durumundaki yeri, daha dirençli bir kadroya sahip olduklarını gösteriyor.")
            if (d['goalsAgainst'] / d['playedGames']) < 1.0:
                st.write("- **Savunma Duvarı:** Kalelerini gole kapatma konusunda çok başarılılar, kolay pes etmezler.")
            
            st.error(f"⚠️ **{dep} Neden Kaybedebilir? (Dezavantajlar)**")
            if (d['goalsFor'] / d['playedGames']) < 1.2:
                st.write("- **Kısır Hücum:** Forvetlerin gol performansı düşük; taktiksel olarak gol bulmakta zorlanabilirler.")
            st.write("- **Deplasman Baskısı:** Rakip sahanın baskısı altında taktiksel hatalar ve konsantrasyon kaybı yaşanabilir.")

        # NİHAİ AI YORUMU
        st.divider()
        st.subheader("🤖 Yapay Zeka Sonuç Özeti")
        fark = (e['points'] / e['playedGames']) - (d['points'] / d['playedGames'])
        
        if fark > 0.4:
            st.write(f"Sistemimiz **{ev}** takımını favori görüyor. Temel neden: Rakibine göre çok daha dengeli bir hücum/savunma dengesine sahip olmaları.")
        elif fark < -0.4:
            st.write(f"Sistemimiz **{dep}** takımını favori görüyor. Temel neden: Deplasmanda olmalarına rağmen ligin en dirençli takımlarından biri olmaları.")
        else:
            st.write("Bu maç taktiksel bir satranç gibi geçecek. İki takımın da birbirine üstünlük kurması zor görünüyor; beraberlik kokusu var.")

except Exception as e:
    st.error("Veriler alınırken bir hata oluştu. API limitinizi kontrol edin.")
