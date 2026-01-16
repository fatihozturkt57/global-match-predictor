import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz v3", layout="wide")
st.title("⚽ Gerçek Veri Tabanlı Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    return res['standings'][0]['table']

try:
    tablo = veri_cek(ligler[sec_lig])
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col1, col2 = st.columns(2)
    with col1: ev = st.selectbox("Ev Sahibi", takimlar)
    with col2: dep = st.selectbox("Deplasman", takimlar)

    if st.button("🔍 TAKIM KARAKTERİNİ ANALİZ ET"):
        e, d = veriler[ev], veriler[dep]
        
        # --- TAKIM KARAKTERİ HESAPLAMA (Gerçek Tablo Verisinden) ---
        def karakter_analizi(t):
            win_rate = t['won'] / t['playedGames']
            gf_rate = t['goalsFor'] / t['playedGames']
            ga_rate = t['goalsAgainst'] / t['playedGames']
            
            # Karakter Belirleme
            if win_rate > 0.6 and gf_rate > 2: style = "Hücum Makinesi"
            elif ga_rate < 1.0: style = "Savunma Duvarı"
            elif win_rate < 0.3: style = "Formsuz / Dirençsiz"
            else: style = "Dengeli / Taktiksel"
            
            return {"win": win_rate, "gf": gf_rate, "ga": ga_rate, "style": style}

        e_analiz = karakter_analizi(e)
        d_analiz = karakter_analizi(d)

        # --- GERÇEKÇİ İSTATİSTİK ALGORİTMASI ---
        # Korner: Hücum gücü yüksek ve dengeli maçlarda artar
        korner_tahmin = 8.0 + (e_analiz['gf'] * 1.5) + (d_analiz['gf'] * 0.5)
        
        # Kart: Savunma zayıfsa ve takımlar birbirine yakınsa (rekabet) artar
        rekabet = 1.5 if abs(e_analiz['win'] - d_analiz['win']) < 0.2 else 0.5
        kart_tahmin = 2.0 + (e_analiz['ga'] + d_analiz['ga']) + rekabet

        # İlk Yarı: Güçlü takımlar genelde İY gol atar
        iy_gol_olasili_e = 1 if e_analiz['gf'] > 1.8 else 0
        iy_gol_olasili_d = 1 if d_analiz['gf'] > 2.2 else 0

        # --- PANEL GÖSTERİMİ ---
        st.divider()
        c1, c2 = st.columns(2)
        with c1: st.info(f"🏠 {ev} Stili: **{e_analiz['style']}**")
        with c2: st.info(f"🚀 {dep} Stili: **{d_analiz['style']}**")

        st.subheader("📊 Maç Dinamikleri")
        m1, m2, m3 = st.columns(3)
        m1.metric("Tahmini Korner", f"{round(korner_tahmin)}")
        m2.metric("Tahmini Kart", f"{round(kart_tahmin)}")
        m3.metric("İY Skoru", f"{iy_gol_olasili_e} - {iy_gol_olasili_d}")

        #
