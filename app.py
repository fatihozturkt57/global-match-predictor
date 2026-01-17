import streamlit as st
import requests
import sqlite3
import random

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    pro INTEGER DEFAULT 0
)
""")
conn.commit()

# =========================
# ADMIN KULLANICI OLUŞTURMA
# =========================
admin_username = "admin"
admin_password = "1234"  # İstediğin şifreyi buraya koyabilirsin
c.execute("SELECT * FROM users WHERE username=?", (admin_username,))
if not c.fetchone():
    c.execute("INSERT INTO users (username, password, pro) VALUES (?, ?, ?)",
              (admin_username, admin_password, 1))  # PRO aktif
    conn.commit()

# =========================
# USER FUNCTIONS
# =========================
def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def make_pro(username):
    c.execute("UPDATE users SET pro=1 WHERE username=?", (username,))
    conn.commit()

# =========================
# STREAMLIT SETUP
# =========================
st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("AI Futbol Analiz Platformu")

if "login" not in st.session_state:
    st.session_state.login = None

# =========================
# LOGIN / REGISTER SIDEBAR
# =========================
with st.sidebar:
    if not st.session_state.login:
        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])

        # ---- LOGIN ----
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="login_user")
            p = st.text_input("Şifre", type="password", key="login_pass")
            if st.button("Giriş Yap"):
                user = get_user(u)
                if user:
                    stored_password = str(user[1]).strip()
                    if stored_password == str(p).strip():
                        st.session_state.login = u
                        st.success("Giriş başarılı!")
                        st.rerun()
                    else:
                        st.error("Şifre yanlış")
                else:
                    st.error("Kullanıcı bulunamadı")

        # ---- REGISTER ----
        with tab2:
            ru = st.text_input("Kullanıcı Adı", key="reg_user")
            rpw = st.text_input("Şifre", type="password", key="reg_pass")

            if st.button("Kayıt Ol"):
                if get_user(ru):
                    st.error("Bu kullanıcı adı zaten var")
                else:
                    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (ru, rpw))
                    conn.commit()
                    st.success("Kayıt başarılı, giriş yapabilirsiniz")
    else:
        user = get_user(st.session_state.login)
        st.success(f"Hoş geldin {user[0]}")

        if user[2]:
            st.success("🔥 PRO ÜYELİK AKTİF")
        else:
            st.warning("FREE ÜYELİK")
            st.info("🔒 Pro analizler kilitli")

            if st.button("💳 Pro Satın Al (Demo)"):
                make_pro(user[0])
                st.success("Pro aktif edildi (demo)")
                st.rerun()

        if st.button("Çıkış Yap"):
            st.session_state.login = None
            st.rerun()

# =========================
# AI ANALYSIS SECTION
# =========================
if not st.session_state.login:
    st.stop()

st.header("AI Maç Analizi")

# --- LIGLER ---
ligler = {
    "İngiltere": "PL",
    "İspanya": "PD",
    "İtalya": "SA",
    "Almanya": "BL1",
    "Fransa": "FL1"
}

sec_lig = st.selectbox("Lig Seçin", list(ligler.keys()))

@st.cache_data(show_spinner=False)
def lig_verisi_al(code):
    url = f"https://api.football-data.org/v4/competitions/{code}/standings"
    r = requests.get(url, headers={"X-Auth-Token": "59aad6ae23824eeb9f427e2ed418512e"}, timeout=10)
    r.raise_for_status()
    return r.json()["standings"][0]["table"]

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

    # Ekstra AI göstergeler (demo)
    st.metric("AI Güven Skoru", "81%")
    st.metric("Risk / Denge Seviyesi", "Orta")
    st.metric("Kırılgan Alan Analizi", "Pas Geç Algılanmadı")
