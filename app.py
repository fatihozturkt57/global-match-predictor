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
        
        # --- AI PARAMETRELERİ ---
        e_mac, d_mac = e['playedGames'], d['playedGames']
        
        if e_mac > 0 and d_mac > 0:
            e_hucum = e['goalsFor'] / e_mac
            e_savunma = e['goalsAgainst'] / e_mac
            d_hucum = d['goalsFor'] / d_mac
            d_savunma = d['goalsAgainst'] / d_mac
            
            # AI Tahmin Algoritması
            ai_ev_skor = e_hucum * (d_savunma / 1.1) + 0.25
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

            # --- AI STRATEJİK ANALİZ ---
            col_ev, col_dep = st.columns(2)
            
            with col_ev:
                st.info(f"🏠 {ev_adi} AI Analiz")
                if e_hucum > d_savunma:
                    st.success(f"🔥 **Hücum Avantajı:** Rakip defansı bozacak kapasitede.")
                else:
                    st.error("⚠️ **Hücum Dezavantajı:** Rakip defans bloğu sizi kısıtlayabilir.")
                
                if e_savunma < 1.0:
                    st.success("🛡️ **Defans Gücü:** Kalesini kapatma başarısı yüksek.")

            with col_dep:
                st.info(f"🚀 {dep_adi} AI Analiz")
                if d_hucum > e_savunma:
                    st.success(f"⚡ **Hücum Avantajı:** Kontra ataklarla etkili olabilir.")
                else:
                    st.error("📉 **Hücum Dezavantajı:** Ofansif verimlilik yeterli görünmüyor.")
                
                if d_savunma > 1.5:
                    st.error("❌ **Defans Dezavantajı:** Arka hatta ciddi boşluklar veriliyor.")

            # --- AI GÜVEN ENDEKSİ ---
            st.divider()
            fark = abs(ai_ev_skor - ai_dep_skor)
            güven = min(95.0, round(fark * 50 + 40, 1))
            
            if ai_ev_skor > ai_dep_skor + 0.3:
                st.success(f"💡 **AI Tahmini:** {ev_adi} Galibiyeti | **Güven:** %{güven}")
            elif ai_dep_skor > ai_ev_skor + 0.3:
                st.error(f"💡 **AI Tahmini:** {dep_adi} Sürprizi/Galibiyeti | **Güven:** %{güven}")
            else:
                st.warning(f"💡 **AI Tahmini:** Beraberlik İhtimali Yüksek | **Güven:** %{60}")
        else:
            st.warning("Seçilen takımların henüz yeterli verisi (oynanmış maçı) yok.")

else:
    st.error("Lig verileri yüklenemedi. API anahtarını kontrol edin.")
