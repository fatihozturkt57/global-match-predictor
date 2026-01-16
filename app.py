import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Maç Çarpıştırma Simülatörü", layout="wide")
st.title("⚽ Takım Karşılaştırmalı Analiz Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_getir(kod):
    try:
        url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
        response = requests.get(url, headers=HEADERS)
        return response.json()['standings'][0]['table']
    except:
        return None

tablo = veri_getir(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman", takimlar)

    if st.button("🚀 MAÇI SİMÜLE ET"):
        ev, dep = veriler[ev_adi], veriler[dep_adi]
        
        # --- ÖZEL KARŞILAŞTIRMA METRİKLERİ ---
        # 1. Hücum vs Savunma Dengesi
        ev_hucum_gucu = ev['goalsFor'] / ev['playedGames']
        dep_savunma_gucu = dep['goalsAgainst'] / dep['playedGames']
        
        dep_hucum_gucu = dep['goalsFor'] / dep['playedGames']
        ev_savunma_gucu = ev['goalsAgainst'] / ev['playedGames']

        # 2. Maç Karakteristiği Belirleme (Eşleşmeye Özel)
        # Eğer ev sahibi çok atıyor, deplasman çok yiyorsa: "TEK KALE MAÇ"
        # Eğer ikisi de az yiyorsa: "KÖRDÜĞÜM MAÇ"
        
        st.divider()
        st.subheader(f"🏟️ Eşleşme Analizi: {ev_adi} vs {dep_adi}")

        # --- DİNAMİK SENARYO ÜRETİCİ ---
        if ev_hucum_gucu > 2.0 and dep_savunma_gucu > 1.5:
            senaryo = "🔥 **YÜKSEK TEMPO:** Ev sahibi hücum hattı, deplasmanın zayıf savunmasını sürklase edebilir. Erken gol beklentisi yüksek."
            korner = 11
            kart = 3
        elif ev_savunma_gucu < 1.0 and dep_savunma_gucu < 1.0:
            senaryo = "🛡️ **STRATEJİK SAVAŞ:** İki takım da savunma disiplinine sahip. Az gollü, satranç gibi bir maç bekliyoruz."
            korner = 7
            kart = 5
        elif dep_hucum_gucu > ev_hucum_gucu:
            senaryo = "⚠️ **DEPLASMAN BASKISI:** Deplasman takımı kağıt üzerinde daha üretken. Ev sahibi kontra atak kollamalı."
            korner = 9
            kart = 6
        else:
            senaryo = "⚖️ **DENGELİ REKABET:** İki takımın güçleri birbirine yakın. Orta saha mücadelesi maçın sonucunu belirler."
            korner = 9
            kart = 4

        # --- GÖRSEL SONUÇLAR ---
        st.warning(senaryo)
        
        col_a, col_b, col_c = st.columns(3)
