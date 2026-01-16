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
        
        e_mac, d_mac = e['playedGames'], d['playedGames']
        
        if e_mac > 0 and d_mac > 0:
            e_hucum = e['goalsFor'] / e_mac
            e_savunma = e['goalsAgainst'] / e_mac
            d_hucum = d['goalsFor'] / d_mac
            d_savunma = d['goalsAgainst'] / d_mac
            
            # Ham veriler (xG)
            ham_ev = e_hucum * (d_savunma / 1.1) + 0.25
            ham_dep = d_hucum * (e_savunma / 1.1)
            
            # --- DÜZELTİLMİŞ GERÇEK SKORLAR ---
            final_ev = round(ham_ev)
            final_dep = round(ham_dep)
            
            # İY Skoru (Hücum güçlerine göre net skor)
            iy_ev_skor = 1 if ham_ev > 1.6 else 0
            iy_dep_skor = 1 if ham_dep > 1.9 else 0

            st.divider()
            st.subheader(f"🤖 AI Tahmin Raporu: {ev_adi} vs {dep_adi}")

            # --- TAHMİN METRİKLERİ ---
            m1, m2, m3, m4 = st.columns(4)
            # Beklenen skor artık net sayı (Örn: 2 - 1)
            m1.metric("MS Tahmini Skor", f"{final_ev} - {final_dep}")
            m2.metric("İY Tahmini Skor", f"{iy_ev_skor} - {iy_dep_skor}")
            m3.metric("Tahmini Korner", f"{int(7.5 + (e_hucum + d_hucum) * 1.6)}+")
            m4.metric("Tahmini Kart", f"{int(2 + (e_savunma + d_savunma) * 1.4)}+")

            st.write(f"ℹ️ *AI Notu: Maçın gol üretme potansiyeli (xG): {round(ham_ev, 1)} - {round(ham_dep, 1)}*")

            st.divider()

            # --- AI STRATEJİK ANALİZ ---
            col_ev, col_dep = st.columns(2)
            
            with col_ev:
                st.info(f"🏠 {ev_adi} AI Analiz")
                if e_hucum > d_savunma:
                    st.success("🔥 **Hücum Avantajı:** Rakip defansı bozacak kapasitede.")
                else:
                    st.error("⚠️ **Hücum Dezavantajı:** Rakip defans bloğu sizi kısıtlayabilir.")
                
                if e_savunma < 1.0:
                    st.success("🛡️ **Defans Gücü:** Kalesini kapat
