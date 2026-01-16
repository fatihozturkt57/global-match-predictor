import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Veri Analiz Paneli", layout="wide")
st.title("📊 Veri Odaklı Maç Analiz Motoru")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def lig_verisi_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table']
    except:
        return None

tablo = lig_verisi_al(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman", takimlar)

    if st.button("📊 VERİLERİ ÇARPIŞTIR"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # --- MATEMATİKSEL HESAPLAMA MOTORU ---
        e_mac = e['playedGames']
        d_mac = d['playedGames']
        
        # Maç Başı Ortalamalar
        e_atilan = e['goalsFor'] / e_mac
        e_yenilen = e['goalsAgainst'] / e_mac
        d_atilan = d['goalsFor'] / d_mac
        d_yenilen = d['goalsAgainst'] / d_mac

        # --- 1. SKOR ANALİZİ (Göreceli Hesaplama) ---
        # Ev sahibinin skoru: Kendi gol atma gücü + Rakibin gol yeme zafiyeti
        skor_ev_hesap = (e_atilan + d_yenilen) / 2 + 0.3 # +0.3 Ev sahibi avantajı
        skor_dep_hesap = (d_atilan + e_yenilen) / 2
        
        final_ev = round(skor_ev_hesap)
        final_dep = round(skor_dep_hesap)

        # --- 2. AVANTAJ / DEZAVANTAJ (Gerçek Rakamlarla) ---
        st.divider()
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader(f"🏠 {ev_adi} Analizi")
            # Dinamik Avantaj/Dezavantaj Kontrolü
            if e_atilan > 1.8: 
                st.success(f"✅ **Hücum Avantajı:** Maç başı {round(e_atilan, 2)} gol atıyor.")
            if e_yenilen > 1.3: 
                st.error(f"❌ **Savunma Dezavantajı:** Maç başı {round(e_yenilen, 2)} gol yiyor.")
            else:
                st.success(f"✅ **Savunma Gücü:** Maç başı sadece {round(e_yenilen, 2)} gol yiyerek kalesini iyi savunuyor.")

        with col2:
            st.subheader(f"🚀 {dep_adi} Analizi")
            if d_atilan > e_atilan:
                st.success(f"✅ **Hücum Üstünlüğü:** Rakibinden daha yüksek gol ortalamasına ({round(d_atilan, 2)}) sahip.")
            if d_yenilen > 1.5:
                st.error(f"❌ **Defans Zafiyeti:** {round(d_yenilen, 2)} gol yeme ortalaması risk teşkil ediyor.")
            if d['won'] > e['won']:
                st.success(f"✅ **Galibiyet Oranı:** Lig genelinde rakibinden daha fazla maç kazandı.")

        # --- 3. İSTATİSTİKSEL TAHMİNLER ---
        st.divider()
        st.subheader("📋 Maç Tahminleri (Veriye Dayalı)")
        
        k1, k2, k3, k4 = st.columns(4)
        
        # İY Skoru: Genelde maçın ilk yarısında toplam golün %40'ı atılır.
        iy_ev = 1 if skor_ev_hesap > 1.7 else 0
        iy_dep = 1 if skor_dep_hesap > 1.9 else 0
        
        # Korner: Takımların toplam gol beklentisi (xG) ile doğru orantılıdır.
        korner = round(7.5 + (e_atilan + d_atilan) * 1.2)
        
        # Kart: Maçtaki savunma zafiyetleri ve rekabet puanına göre.
        kart = round(2.0 + (e_yenilen + d_yenilen) * 1.4)

        k1.metric("Maç Sonu Tahmini", f"{final_ev} - {final_dep}")
        k2.metric("İlk Yarı Skoru", f"{iy_ev} - {iy_dep}")
        k3.metric("Tahmini Korner", f"{korner}+")
