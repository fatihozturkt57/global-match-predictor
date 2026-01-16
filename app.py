import streamlit as st
import requests

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("AI Veri Madenciliği & Stratejik Analiz")

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
    # 1️⃣ AI GÜVEN SKORU
    # =========================
    guven_skoru = min(100, round(abs(ev_oran - dep_oran) * 1.5))

    # =========================
    # 2️⃣ RİSK / DENGE SEVİYESİ
    # =========================
    if abs(ev_oran - dep_oran) < 10:
        risk = "Yüksek Risk – Sürprize Açık"
    elif abs(ev_oran - dep_oran) < 25:
        risk = "Orta Risk – Dengeli Maç"
    else:
        risk = "Düşük Risk – Net Favori"

    # =========================
    # 3️⃣ KIRILGAN ALAN ANALİZİ
    # =========================
    def kirilgan_alan(h, s):
        if s > h:
            return "Savunma Kırılgan"
        elif h > s:
            return "Hücum Güçlü"
        else:
            return "Denge Zayıf"

    ev_kirilgan = kirilgan_alan(e_h, e_s)
    dep_kirilgan = kirilgan_alan(d_h, d_s)

    # =========================
    # AVANTAJ / DEZAVANTAJ (ZORUNLU)
    # =========================
    def avantaj_dezavantaj(h, s):
        if h > s:
            return "Hücum Etkinliği Avantaj", "Savunma Açıkları Dezavantaj"
        else:
            return "Savunma Direnci Avantaj", "Hücum Üretkenliği Dezavantaj"

    ev_av, ev_dez = avantaj_dezavantaj(e_h, e_s)
    dep_av, dep_dez = avantaj_dezavantaj(d_h, d_s)

    # =========================
    # GÖRSEL RAPOR
    # =========================
    st.divider()
    st.header(f"{ev_adi} - {dep_adi} AI Raporu")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ev Sahibi XG", round(ev_xg, 2))
        st.metric("Ev Galibiyet %", f"%{ev_oran}")
    with m2:
        st.metric("Deplasman XG", round(dep_xg, 2))
        st.metric("Deplasman Galibiyet %", f"%{dep_oran}")
    with m3:
        st.metric("AI Güven Skoru", f"%{guven_skoru}")
        st.metric("Risk Seviyesi", risk)

    st.subheader("🔍 Taktiksel Analiz")

    a1, a2 = st.columns(2)
    with a1:
        st.markdown(f"**{ev_adi} Avantajı:** {ev_av}")
        st.markdown(f"**{ev_adi} Dezavantajı:** {ev_dez}")
        st.markdown(f"**Kırılgan Alan:** {ev_kirilgan}")

    with a2:
        st.markdown(f"**{dep_adi} Avantajı:** {dep_av}")
        st.markdown(f"**{dep_adi} Dezavantajı:** {dep_dez}")
        st.markdown(f"**Kırılgan Alan:** {dep_kirilgan}")
