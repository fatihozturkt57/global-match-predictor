import streamlit as st
import requests

# =========================
# API AYARLARI
# =========================
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

st.set_page_config(page_title="AI Pro Analiz", layout="wide")
st.title("AI Veri Madenciliği & Stratejik Analiz")

# =========================
# SESSION / USER DB
# =========================
if "users" not in st.session_state:
    st.session_state.users = {
        "admin": {
            "password": "123456",
            "email": "admin@system.ai",
            "phone": "0000000000",
            "pro": True
        }
    }

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# =========================
# KULLANICI PANELİ
# =========================
st.sidebar.subheader("👤 Kullanıcı Paneli")

if not st.session_state.logged_in:
    tab1, tab2 = st.sidebar.tabs(["🔑 Giriş", "📝 Kayıt"])

    with tab1:
        u = st.text_input("Kullanıcı Adı", key="login_user")
        p = st.text_input("Şifre", type="password", key="login_pass")

        if st.button("Giriş Yap", key="login_btn"):
            if u in st.session_state.users and st.session_state.users[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.current_user = u
                st.rerun()
            else:
                st.error("Hatalı bilgiler")

    with tab2:
        ru = st.text_input("Yeni Kullanıcı Adı", key="reg_user")
        rm = st.text_input("E-posta", key="reg_mail")
        rp = st.text_input("Telefon", key="reg_phone")
        rpass = st.text_input("Şifre", type="password", key="reg_pass")

        if st.button("Kayıt Ol", key="reg_btn"):
            if ru in st.session_state.users:
                st.error("Bu kullanıcı adı alınmış")
            elif not ru or not rpass:
                st.error("Zorunlu alanlar boş")
            else:
                st.session_state.users[ru] = {
                    "password": rpass,
                    "email": rm,
                    "phone": rp,
                    "pro": False
                }
                st.success("Kayıt başarılı")

else:
    user = st.session_state.current_user
    udata = st.session_state.users[user]

    st.sidebar.success(f"👋 Hoş geldin: {user}")

    if udata["pro"]:
        st.sidebar.success("🔥 PRO ÜYELİK AKTİF")
    else:
        st.sidebar.warning("🆓 FREE ÜYELİK")
        if st.sidebar.button("🔥 Pro’ya Geç (Demo)", key="upgrade_btn"):
            st.session_state.users[user]["pro"] = True
            st.rerun()

    if st.sidebar.button("Çıkış Yap", key="logout_btn"):
        st.session_state.logged_in = False
        st.session_state.current_user = None
        st.rerun()

# =========================
# GİRİŞ ZORUNLU
# =========================
if not st.session_state.logged_in:
    st.warning("Devam etmek için giriş yapmalısın")
    st.stop()

# =========================
# LİG VERİLERİ
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

sec_lig = st.sidebar.selectbox("Lig Seçin", list(ligler.keys()), key="lig_sec")
tablo = lig_verisi_al(ligler[sec_lig])

takimlar_db = {row["team"]["name"]: row for row in tablo}
isimler = sorted(takimlar_db.keys())

c1, c2 = st.columns(2)
with c1:
    ev_adi = st.selectbox("Ev Sahibi", isimler, key="ev")
with c2:
    dep_adi = st.selectbox("Deplasman", isimler, key="dep")

# =========================
# ANALİZ
# =========================
if st.button("AI ANALİZİ BAŞLAT", key="analyze_btn"):
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
        st.metric("Ev XG", round(ev_xg, 2))
        st.metric("Ev Galibiyet %", ev_oran)
    with m2:
        st.metric("Dep XG", round(dep_xg, 2))
        st.metric("Dep Galibiyet %", dep_oran)

    # =========================
    # PAS GEÇ + PRO GÖRÜNÜRLÜK
    # =========================
    if udata["pro"]:
        fark = abs(ev_xg - dep_xg)

        if fark < 0.15:
            st.error("⛔ AI PAS GEÇ UYARISI: Bu maç istatistiksel olarak oynanmaya uygun değil.")
        else:
            st.success("🔥 PRO AI ONAYI: Bu maç Pro kriterlerine göre analiz edildi.")
