import streamlit as st
import requests
import random
import sqlite3
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

# =========================
# SENDGRID AYARLARI
# =========================
SENDGRID_API_KEY = st.secrets["SENDGRID_API_KEY"]
SENDGRID_FROM_EMAIL = st.secrets["SENDGRID_FROM_EMAIL"]

# =========================
# FOOTBALL API
# =========================
API_KEY = "59aad6ae23824eeb9f427e2ed418512e"
HEADERS = {"X-Auth-Token": API_KEY}

# =========================
# DATABASE
# =========================
conn = sqlite3.connect("users.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    email TEXT,
    phone TEXT,
    pro INTEGER DEFAULT 0,
    verified INTEGER DEFAULT 0
)
""")
conn.commit()

# =========================
# SENDGRID E-POSTA FONKSİYONU
# =========================
def send_email(to, code):
    try:
        message = Mail(
            from_email=SENDGRID_FROM_EMAIL,
            to_emails=to,
            subject="AI Platform Doğrulama Kodu",
            html_content=f"""
            <h2>AI Platform</h2>
            <p>Doğrulama Kodunuz:</p>
            <h1>{code}</h1>
            <p>Bu kodu kimseyle paylaşmayın.</p>
            """
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        sg.send(message)
        return True

    except Exception:
        st.error("E-posta gönderilemedi. Lütfen daha sonra tekrar deneyin.")
        return False

# =========================
# KULLANICI FONKSİYONLARI
# =========================
def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def make_pro(username):
    c.execute("UPDATE users SET pro=1 WHERE username=?", (username,))
    conn.commit()

# =========================
# STREAMLIT AYARLARI
# =========================
st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("AI Futbol Analiz Platformu")

if "login" not in st.session_state:
    st.session_state.login = None

# =========================
# KULLANICI GİRİŞ / KAYIT
# =========================
with st.sidebar:
    if not st.session_state.login:
        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])

        # ---- GİRİŞ ----
        with tab1:
            u = st.text_input("Kullanıcı Adı", key="login_user")
            p = st.text_input("Şifre", type="password", key="login_pass")
            if st.button("Giriş Yap"):
                user = get_user(u)
                if user and user[1] == p and user[5] == 1:
                    st.session_state.login = u
                    st.rerun()
                else:
                    st.error("Giriş başarısız veya hesap doğrulanmamış")

        # ---- KAYIT ----
        with tab2:
            ru = st.text_input("Kullanıcı Adı", key="reg_user")
            rm = st.text_input("E-posta", key="reg_mail")
            rp = st.text_input("Telefon", key="reg_phone")
            rpw = st.text_input("Şifre", type="password", key="reg_pass")

            if st.button("E-posta Kodu Gönder"):
                code = random.randint(100000, 999999)
                st.session_state.email_code = code
                if send_email(rm, code):
                    st.success("Doğrulama kodu e-posta ile gönderildi")

            rc = st.text_input("Doğrulama Kodu", key="reg_code")

            if st.button("Kayıt Ol"):
                if "email_code" not in st.session_state:
                    st.error("Önce kod gönderin")
                elif str(rc) != str(st.session_state.email_code):
                    st.error("Kod hatalı")
                else:
                    try:
                        c.execute(
                            "INSERT INTO users VALUES (?,?,?,?,0,1)",
                            (ru, rpw, rm, rp)
                        )
                        conn.commit()
                        st.success("Kayıt başarılı, giriş yapabilirsiniz")
                    except:
                        st.error("Bu kullanıcı adı zaten var")

    else:
        user = get_user(st.session_state.login)
        st.success(f"Hoş geldin {user[0]}")

        if user[4]:
            st.success("🔥 PRO ÜYELİK AKTİF")
        else:
            st.warning("FREE ÜYELİK")
            st.info("🔒 Pro analizler kilitli")

            if st.button("💳 Pro Satın Al (Demo)"):
                make_pro(user[0])
                st.success("Ödeme alındı → Pro aktif")
                st.rerun()

        if st.button("Çıkış Yap"):
            st.session_state.login = None
            st.rerun()

# =========================
# AI ANALİZ BÖLÜMÜ
# =========================
if not st.session_state.login:
    st.stop()

st.header("AI Maç Analizi")

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
    r = requests.get(url, headers=HEADERS, timeout=10)
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

    # Ekstra AI göstergeler
    st.metric("AI Güven Skoru", "81%")
    st.metric("Risk / Denge Seviyesi", "Orta")
    st.metric("Kırılgan Alan Analizi", "Pas Geç Algılanmadı")
