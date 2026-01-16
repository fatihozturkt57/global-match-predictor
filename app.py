import streamlit as st
import requests

# API Ayarları
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {'X-Auth-Token': API_KEY}

st.set_page_config(page_title="Pro Analiz v8", layout="wide")
st.title("⚽ Veri Odaklı Maç Karşılaştırma Sistemi")

ligler = {"İngiltere": "PL", "İspanya": "PD", "İtalya": "SA", "Almanya": "BL1", "Fransa": "FL1"}
sec_lig = st.sidebar.selectbox("Ligi Seçin", list(ligler.keys()))

@st.cache_data
def veri_al(kod):
    url = f"https://api.football-data.org/v4/competitions/{kod}/standings"
    try:
        res = requests.get(url, headers=HEADERS).json()
        return res['standings'][0]['table']
    except:
        return None

tablo = veri_al(ligler[sec_lig])

if tablo:
    veriler = {row['team']['name']: row for row in tablo}
    takimlar = sorted(list(veriler.keys()))

    c1, c2 = st.columns(2)
    with c1: ev_adi = st.selectbox("Ev Sahibi Takım", takimlar)
    with c2: dep_adi = st.selectbox("Deplasman Takımı", takimlar)

    if st.button("🔍 VERİLERİ ÇARPIŞTIR VE ANALİZ ET"):
        # Takım verilerini güvenli bir şekilde çekelim
        e = veriler.get(ev_adi)
        d = veriler.get(dep_adi)
        
        if e and d:
            # Maç başı istatistikleri (Analizin temeli)
            e_mac, d_mac = e['playedGames'], d['playedGames']
            
            # 0'a bölme hatasını engellemek için kontrol
            if e_mac > 0 and d_mac > 0:
                e_at = e['goalsFor'] / e_mac
                e_ye = e['goalsAgainst'] / e_mac
                d_at = d['goalsFor'] / d_mac
                d_ye = d['goalsAgainst'] / d_mac

                # --- ÇARPIŞTIRMALI ANALİZ ---
                # Ev sahibinin gol gücü rakibin defans zafiyetiyle ölçülür
                e_xg = (e_at + d_ye) / 2 + 0.25 # 0.25 Ev sahibi avantajı
                d_xg = (d_at + e_ye) / 2

                st.divider()
                # Hatalı olan satırı bu şekilde güvenli hale getirdik:
                baslik = f"🏟️ {ev_adi} vs {dep_adi} Karşılaştırmalı Analiz"
                st.subheader(baslik)

                m1, m2, m3, m4 = st.columns(4)
                # Ondalıklı skorlar her maça özel veri olduğunu kanıtlar
                m1.metric("Beklenen Skor (xG)", f"{round(e_xg, 1)} - {round(d_xg, 1)}")
                m2.metric("İlk Yarı Beklentisi", f"{int(e_xg*0.45)} - {int(d_xg*0.4)}")
                m3.metric("Tahmini Korner", f"{round(7 + (e_at + d_at) * 1.8)}+")
                m4.metric("Tahmini Kart", f"{round(2 + (e_ye + d_ye) * 1.5)}+")

                st.divider()
                st.subheader("⚖️ Avantaj & Dezavantaj Dengesi")
                a1, a2 = st.columns(2)

                with a1:
                    st.info(f"🏠 {ev_adi}")
                    if e_at > d_ye:
                        st.success(f"✅ **AVANTAJ:** Hücum hattınız ({round(e_at, 1)}), rakibin savunma zafiyetinden ({round(d_ye, 1)}) daha üstün.")
                    else:
                        st.error("❌ **DEZAVANTAJ:** Rakip savunma sizin gol yollarınızı kilitleyebilir.")
                    
                    if e_ye < 1.1:
                        st.success("✅ **AVANTAJ:** İç sahada çok düşük gol yeme oranı.")

                with a2:
                    st.info(f"🚀 {dep_adi}")
                    if d_at > e_ye:
                        st.success(f"✅ **AVANTAJ:** Deplasman hücumunuz ev sahibi defansını hataya zorlayabilir.")
                    else:
                        st.error("❌ **DEZAVANTAJ:** Ev sahibi savunma disiplini karşısında skor üretmek zor olabilir.")
                    
                    if d_ye > 1.4:
                        st.error(f"❌ **DEZAVANTAJ:** Maç başı {round(d_ye, 1)} gol yeme ortalaması defansif bir risk.")

                st.divider()
                # Maç Özeti (Veriye dayalı)
                if e_xg > d_xg + 0.4:
                    st.info(f"💡 **Analiz:** {ev_adi} verileri net bir galibiyet ihtimali gösteriyor.")
                elif d_xg > e_xg + 0.4:
                    st.info(f"💡 **Analiz:** {dep_adi} bu zorlu deplasmanda sürprize açık verilere sahip.")
                else:
                    st.info("💡 **Analiz:** Güç dengeleri çok yakın, beraberlik veya tek farklı skor muhtemel.")
            else:
                st.warning("Seçilen takımların henüz oynanmış maçı bulunmuyor.")
else:
    st.error("Lig verileri yüklenemedi. Lütfen API anahtarınızı veya internetinizi kontrol edin.")
