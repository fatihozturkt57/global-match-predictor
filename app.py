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

    st.divider()
    st.header(f"{ev_adi} - {dep_adi} AI Raporu")

    m1, m2 = st.columns(2)
    with m1:
        st.metric("Ev Sahibi XG", round(ev_xg, 2))
        st.metric("Ev Galibiyet %", f"%{ev_oran}")
    with m2:
        st.metric("Deplasman XG", round(dep_xg, 2))
        st.metric("Deplasman Galibiyet %", f"%{dep_oran}")

    st.divider()
    st.subheader("Avantaj / Dezavantaj Nedenleri")

    av_col, dez_col = st.columns(2)

    with av_col:
        st.markdown("### Avantaj Nedenleri")
        if ev_xg > dep_xg:
            st.write(f"- {ev_adi}, daha yüksek gol beklentisine sahip.")
        if e_h > d_h:
            st.write(f"- {ev_adi}, hücumda daha üretken.")
        if e_s < d_s:
            st.write(f"- {ev_adi}, savunmada daha sağlam.")
        if ev_oran >= 55:
            st.write("- İstatistiksel üstünlük ev sahibinde.")

    with dez_col:
        st.markdown("### Dezavantaj Nedenleri")
        if dep_xg >= ev_xg:
            st.write(f"- {dep_adi}, dengeyi bozabilecek hücum gücüne sahip.")
        if e_s > d_s:
            st.write(f"- {ev_adi}, savunmada rakibinden daha fazla gol yiyor.")
        if ev_oran < 55:
            st.write("- Galibiyet ihtimali net değil.")
        if abs(ev_xg - dep_xg) < 0.30:
            st.write("- Güç farkı düşük, sürpriz ihtimali var.")
