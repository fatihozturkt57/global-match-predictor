import streamlit as st
import requests

# Senin API anahtarın
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = { 'X-Auth-Token': API_KEY }

# Sayfa Tasarımı
st.set_page_config(page_title="Global Tahmin Paneli", page_icon="⚽", layout="centered")

st.title("⚽ AI Destekli Maç Analiz Sistemi")
st.markdown("Dünya liglerinden canlı verilerle saniyelik tahmin üretir.")

# Ligleri Tanımlayalım
ligler = {
    "İngiltere Premier Lig": "PL",
    "İspanya La Liga": "PD",
    "İtalya Serie A": "SA",
    "Almanya Bundesliga": "BL1",
    "Fransa Ligue 1": "FL1",
    "Portekiz Premier Lig": "PPL",
    "Hollanda Eredivisie": "DED"
}

secilen_lig = st.selectbox("Analiz edilecek ligi seçin:", list(ligler.keys()))

@st.cache_data # Sayfa her yenilendiğinde veriyi tekrar çekmemesi için
def veri_getir(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    res = requests.get(url, headers=HEADERS).json()
    # Puan durumunu bir sözlüğe çeviriyoruz
    return {row['team']['name']: row for row in res['standings'][0]['table']}

try:
    takimlar_verisi = veri_getir(ligler[secilen_lig])
    takim_listesi = sorted(list(takimlar_verisi.keys()))

    col1, col2 = st.columns(2)
    with col1:
        ev = st.selectbox("Ev Sahibi Takım", takim_listesi)
    with col2:
        dep = st.selectbox("Deplasman Takımı", takim_listesi)

    if st.button("MAÇI ANALİZ ET"):
        e_v = takimlar_verisi[ev]
        d_v = takimlar_verisi[dep]
        
        # Matematiksel Analiz (Puan ve Gol Dengesi)
        ev_puan = (e_v['points'] / e_v['playedGames']) + (e_v['goalsFor'] / 40) + 0.3
        dep_puan = (d_v['points'] / d_v['playedGames']) + (d_v['goalsFor'] / 40)
        
        st.divider()
        st.subheader("🤖 Yapay Zeka Tahmini")
        
        if ev_puan > dep_puan + 0.35:
            st.success(f"🏆 Favori: **{ev}** (Maç Sonucu: 1)")
        elif dep_puan > ev_puan + 0.35:
            st.error(f"🏆 Favori: **{dep}** (Maç Sonucu: 2)")
        else:
            st.warning("🤝 Denge: **Beraberlik İhtimali Yüksek** (Maç Sonucu: 0)")
            
        st.info(f"💡 İpucu: {ev} şu an {e_v['points']} puanda, {dep} ise {d_v['points']} puanda.")

except Exception as e:
    st.error("Ücretsiz API limitine takılmış olabiliriz veya bu lig şu an erişime kapalı. Lütfen başka bir lig deneyin.")
