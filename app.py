import streamlit as st
import requests

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("AI Veri Madenciliği & Stratejik Analiz")

# =========================
# PREMIUM MOD
# =========================
premium = st.sidebar.toggle("🔥 Pro Modu Aç", value=False)

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

c1, c2 = st.columns(2)
with c1:
    ev_adi = st.selectbox("Ev Sahibi", isimler)
with c2:
    dep_adi = st.selectbox("Deplasman", isimler)

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

    toplam_xg = ev_xg + dep_xg
    ev_oran = round((ev_xg / toplam_xg) * 100)
    dep_oran = 100 - ev_oran

    # =========================
    # AI GÜVEN & RİSK
    # =========================
    guven = min(100, round(abs(ev_oran - dep_oran) * 1.5))

    if abs(ev_oran - dep_oran) < 10:
        risk = "Yüksek Risk – Dengeli"
    elif abs(ev_oran - dep_oran) < 25:
        risk = "Orta Risk"
    else:
        risk = "Düşük Risk – Net Taraf"

    # =========================
    # FORM (YAKLAŞIK)
    # =========================
    def form_hesap(puan, mac):
        oran = puan / max(mac * 3, 1)
        if oran > 0.6:
            return "İyi Form"
        elif oran > 0.4:
            return "Orta Form"
        else:
            return "Zayıf Form"

    ev_form = form_hesap(e["points"], e_mac)
    dep_form = form_hesap(d["points"], d_mac)

    # =========================
    # AVANTAJ / DEZAVANTAJ
    # =========================
    def av_dez(h, s):
        if h > s:
            return "Hücum Gücü", "Savunma Açıkları"
        else:
            return "Savunma Direnci", "Hücum Zayıflığı"

    ev_av, ev_dez = av_dez(e_h, e_s)
    dep_av, dep_dez = av_dez(d_h, d_s)

    # =========================
    # RAPOR
    # =========================
    st.divider()
    st.header(f"{ev_adi} - {dep_adi} AI Maç Raporu")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ev XG", round(ev_xg, 2))
        st.metric("Ev %", f"%{ev_oran}")
    with m2:
        st.metric("Dep XG", round(dep_xg, 2))
        st.metric("Dep %", f"%{dep_oran}")
    with m3:
        st.metric("AI Güven", f"%{guven}")
        st.metric("Risk", risk)

    if premium:
        st.subheader("🔥 Pro Analiz")
        p1, p2 = st.columns(2)
        with p1:
            st.write(f"**{ev_adi} Form:** {ev_form}")
            st.write(f"Avantaj: {ev_av}")
            st.write(f"Dezavantaj: {ev_dez}")
        with p2:
            st.write(f"**{dep_adi} Form:** {dep_form}")
            st.write(f"Avantaj: {dep_av}")
            st.write(f"Dezavantaj: {dep_dez}")
    else:
        st.info("🔒 Detaylı analiz için Pro Modu aç")
