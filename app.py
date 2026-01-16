import streamlit as st
import requests

# =========================
# API
# =========================
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("AI Veri Madenciliği & Stratejik Analiz")

# =========================
# SESSION
# =========================
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "pro" not in st.session_state:
    st.session_state.pro = False

# =========================
# USER PANEL
# =========================
st.sidebar.divider()
st.sidebar.subheader("👤 Kullanıcı Paneli")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["Giriş", "Kayıt"])

    with tab1:
        user = st.text_input("Kullanıcı Adı")
        pwd = st.text_input("Şifre", type="password")
        if st.button("Giriş Yap"):
            if user and pwd:
                st.session_state.logged_in = True
                st.success("Giriş başarılı")

    with tab2:
        st.text_input("Kullanıcı Adı")
        st.text_input("E-posta")
        st.text_input("Telefon")
        st.text_input("Şifre", type="password")
        if st.button("Kayıt Ol"):
            st.success("Kayıt oluşturuldu (Demo)")

else:
    st.sidebar.success("Giriş yapıldı")

    if not st.session_state.pro:
        st.sidebar.warning("🆓 Free Üyelik")
        if st.sidebar.button("🔥 Pro’ya Geç"):
            st.session_state.pro = True
    else:
        st.sidebar.success("🔥 Pro Üyelik Aktif")

# =========================
# PRO PRICING
# =========================
if st.session_state.logged_in and not st.session_state.pro:
    st.sidebar.divider()
    st.sidebar.subheader("💎 Pro Üyelik")
    st.sidebar.write("Aylık: **149₺**")
    st.sidebar.write("Yıllık: **1499₺**")
    st.sidebar.info("""
**Banka Bilgileri**
Banka: Örnek Banka  
IBAN: TR00 0000 0000 0000 0000 00  
Açıklama: Kullanıcı Adı + Pro
""")

# =========================
# DATA
# =========================
@st.cache_data(show_spinner=False)
def lig_verisi_al(code):
    url = f"https://api.football-data.org/v4/competitions/{code}/standings"
    r = requests.get(url, headers=HEADERS, timeout=10)
    r.raise_for_status()
    return r.json()["standings"][0]["table"]

ligler = {
    "İngiltere": "PL",
    "İspanya": "PD",
    "İtalya": "SA",
    "Almanya": "BL1",
    "Fransa": "FL1"
}

sec_lig = st.sidebar.selectbox("Lig Seçin", list(ligler.keys()))
tablo = lig_verisi_al(ligler[sec_lig])

takimlar_db = {row["team"]["name"]: row for row in tablo}
isimler = sorted(takimlar_db.keys())

lig_h = sum(r["goalsFor"] for r in tablo) / sum(r["playedGames"] for r in tablo)
lig_s = sum(r["goalsAgainst"] for r in tablo) / sum(r["playedGames"] for r in tablo)

c1, c2 = st.columns(2)
with c1:
    ev_adi = st.selectbox("Ev Sahibi", isimler)
with c2:
    dep_adi = st.selectbox("Deplasman", isimler)

# =========================
# ANALYSIS
# =========================
if st.button("AI ANALİZİ BAŞLAT"):
    e = takimlar_db[ev_adi]
    d = takimlar_db[dep_adi]

    e_mac = max(e["playedGames"], 1)
    d_mac = max(d["playedGames"], 1)

    e_h = e["goalsFor"] / e_mac
    e_s = e["goalsAgainst"] / e_mac
    d_h = d["goalsFor"] / d_mac
    d_s = d["goalsAgainst"] / d_mac

    ev_xg = (e_h * d_s) ** 0.5 + 0.25
    dep_xg = (d_h * e_s) ** 0.5

    toplam = ev_xg + dep_xg
    ev_oran = round((ev_xg / toplam) * 100)
    dep_oran = 100 - ev_oran

    fark = abs(ev_oran - dep_oran)
    guven = min(100, round(fark * 1.5))

    def form(puan, mac):
        oran = puan / max(mac * 3, 1)
        if oran > 0.6: return "İyi"
        if oran > 0.4: return "Orta"
        return "Zayıf"

    ev_form = form(e["points"], e_mac)
    dep_form = form(d["points"], d_mac)

    # PAS GEÇ (SADECE PRO)
    pas_gec = False
    if st.session_state.pro:
        sayac = 0
        if fark < 8: sayac += 1
        if guven < 25: sayac += 1
        if ev_form == dep_form: sayac += 1
        pas_gec = sayac >= 2

    def av_dez(h, s):
        if h > lig_h and s < lig_s:
            return "Lig Üstü Performans", "Belirgin Zaaf Yok"
        elif h < lig_h:
            return "Savunma Dengesi", "Hücum Yetersizliği"
        else:
            return "Hücum Gücü", "Savunma Açıkları"

    ev_av, ev_dez = av_dez(e_h, e_s)
    dep_av, dep_dez = av_dez(d_h, d_s)

    st.divider()
    st.header(f"{ev_adi} - {dep_adi} AI Maç Raporu")

    if st.session_state.pro and pas_gec:
        st.error("⛔ AI PAS GEÇ: Pro analizine göre bu maç risklidir.")
    else:
        st.success("✅ AI Analiz: Maç analiz edilebilir.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ev %", f"%{ev_oran}")
    with m2:
        st.metric("Dep %", f"%{dep_oran}")
    with m3:
        st.metric("AI Güven", f"%{guven}")

    if st.session_state.pro:
        st.subheader("🔥 Pro Detay Analiz")
        p1, p2 = st.columns(2)
        with p1:
            st.write(f"{ev_adi} Form: {ev_form}")
            st.write(f"Avantaj: {ev_av}")
            st.write(f"Dezavantaj: {ev_dez}")
        with p2:
            st.write(f"{dep_adi} Form: {dep_form}")
            st.write(f"Avantaj: {dep_av}")
            st.write(f"Dezavantaj: {dep_dez}")
    else:
        st.info("🔒 PAS GEÇ ve detaylı analizler Pro Üyelikte açılır.")
