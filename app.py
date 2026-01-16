import streamlit as st
import requests

API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("AI Veri Madenciliği & Stratejik Analiz")

# =========================
# PRO MOD
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

# =========================
# LİG ORTALAMALARI
# =========================
lig_h = sum(r["goalsFor"] for r in tablo) / sum(r["playedGames"] for r in tablo)
lig_s = sum(r["goalsAgainst"] for r in tablo) / sum(r["playedGames"] for r in tablo)

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

    fark = abs(ev_oran - dep_oran)
    guven = min(100, round(fark * 1.5))

    # =========================
    # FORM
    # =========================
    def form(puan, mac):
        oran = puan / max(mac * 3, 1)
        if oran > 0.6:
            return "İyi"
        elif oran > 0.4:
            return "Orta"
        else:
            return "Zayıf"

    ev_form = form(e["points"], e_mac)
    dep_form = form(d["points"], d_mac)

    # =========================
    # PAS GEÇ (SADECE PRO)
    # =========================
    pas_gec = False
    if premium:
        sayac = 0
        if fark < 8:
            sayac += 1
        if guven < 25:
            sayac += 1
        if ev_form == dep_form:
            sayac += 1
        pas_gec = sayac >= 2

    # =========================
    # AVANTAJ / DEZAVANTAJ
    # =========================
    def av_dez(h, s):
        if h > lig_h and s < lig_s:
            return "Lig Üstü Performans", "Belirgin Zaaf Yok"
        elif h < lig_h:
            return "Savunma Dengesi", "Hücum Yetersizliği"
        else:
            return "Hücum Gücü", "Savunma Açıkları"

    ev_av, ev_dez = av_dez(e_h, e_s)
    dep_av, dep_dez = av_dez(d_h, d_s)

    # =========================
    # RAPOR
    # =========================
    st.divider()
    st.header(f"{ev_adi} - {dep_adi} AI Maç Raporu")

    if premium and pas_gec:
        st.error("⛔ AI PAS GEÇ: Bu maç Pro analizine göre risklidir.")
    else:
        st.success("✅ AI Analiz: Maç analiz edilebilir.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Ev %", f"%{ev_oran}")
    with m2:
        st.metric("Dep %", f"%{dep_oran}")
    with m3:
        st.metric("AI Güven", f"%{guven}")

    if premium:
        st.subheader("🔥 Pro Detay Analiz")
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
        st.info("🔒 PAS GEÇ uyarıları ve detaylı analizler Pro Mod’da açılır.")
