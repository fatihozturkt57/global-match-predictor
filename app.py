import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz v4", layout="wide")
st.title("⚽ Takım Karakter Analiz Sistemi")

ligler = {
    "İngiltere": "PL", 
    "İspanya": "PD", 
    "İtalya": "SA", 
    "Almanya": "BL1", 
    "Fransa": "FL1"
}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_cek(kod):
    try:
        url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
        response = requests.get(url, headers=HEADERS)
        data = response.json()
        return data['standings'][0]['table']
    except:
        return None

tablo = veri_cek(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    col1, col2 = st.columns(2)
    with col1: ev = st.selectbox("Ev Sahibi Takım", takimlar)
    with col2: dep = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 DERİN ANALİZİ BAŞLAT"):
        e, d = veriler[ev], veriler[dep]
        
        # --- TAKIM KARAKTERİSTİK HESAPLAMALARI ---
        e_mac = e['playedGames']
        d_mac = d['playedGames']
        
        # 1. Agresiflik ve Kart Tahmini (Savunma zayıflığına göre)
        # Çok gol yiyen ve puanı az olan takım daha çok faul yapar/kart görür.
        e_sertlik = (e['goalsAgainst'] / e_mac) * 1.5
        d_sertlik = (d['goalsAgainst'] / d_mac) * 1.5
        toplam_kart = 2 + e_sertlik + d_sertlik

        # 2. Korner Tahmini (Hücum baskısına göre)
        # Çok gol atan ve maç kazanan takımlar daha fazla korner kullanır.
        e_baski = (e['goalsFor'] / e_mac) * 2
        d_baski = (d['goalsFor'] / d_mac) * 1.5
        toplam_korner = 6 + e_baski + d_baski

        # 3. İlk Yarı Dinamiği
        # Ev sahibi güçlüyse İY gol bulma ihtimali %60, zayıfsa %20
        iy_ev = 1 if (e['won'] / e_mac) > 0.5 else 0
        iy_dep = 1 if (d['won'] / d_mac) > 0.6 else 0

        # --- SONUÇ EKRANI ---
        st.divider()
        st.subheader(f"📊 {ev} vs {dep} Analizi")
        
        m1, m2, m3 = st.columns(3)
        m1.metric("Beklenen Korner", f"{round(toplam_korner)}+")
        m2.metric("Beklenen Kart", f"{round(toplam_kart)}+")
        m3.metric("İY Tahmini", f"{iy_ev} - {iy_dep}")

        st.divider()
        
        # Takımlara Özel "Neden" Analizi
        c1, c2 = st.columns(2)
        with c1:
            st.info(f"🏠 {ev} Analizi")
            if e['goalsAgainst'] / e_mac > 1.5:
                st.write("⚠️ **Savunma Zafiyeti:** Maç başı yüksek gol yeme oranı sert oynamalarına neden olabilir.")
            if e['goalsFor'] / e_mac > 2:
                st.write("🔥 **Hücum Gücü:** İç sahada baskılı başlayıp korner sayısını artıracaktır.")
        
        with c2:
            st.info(f"🚀 {dep} Analizi")
            if d['won'] / d_mac > 0.6:
                st.write("💪 **Deplasman Formu:** Kazanma alışkanlığı olan, disiplinli bir takım.")
            if d['goalsAgainst'] / d_mac < 1.0:
                st.write("🛡️ **Katı Savunma:** Kolay gol yemiyorlar, bu maçta kart sayısı yükselebilir.")

else:
    st.error("Veri çekilemedi. Lütfen API limitini veya internet bağlantınızı kontrol edin.")
