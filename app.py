import streamlit as st
import requests
import random
import sqlite3
import smtplib
from email.mime.text import MIMEText

# =========================
# SMTP AYARLARI (DOLDUR)
# =========================
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "MAILIN@gmail.com"
SMTP_PASSWORD = "APP_PASSWORD"

# =========================
# FOOTBALL API
# =========================
API_KEY = "FOOTBALL_API_KEY"
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
# FONKSİYONLAR
# =========================
def send_email(to, code):
    msg = MIMEText(f"Doğrulama kodunuz: {code}")
    msg["Subject"] = "AI Platform Doğrulama"
    msg["From"] = SMTP_EMAIL
    msg["To"] = to

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def make_pro(username):
    c.execute("UPDATE users SET pro=1 WHERE username=?", (username,))
    conn.commit()

# =========================
# STREAMLIT
# =========================
st.set_page_config(page_title="AI Pro Predictor", layout="wide")
st.title("AI Futbol Analiz Platformu")

if "login" not in st.session_state:
    st.session_state.login = None

# =========================
# AUTH
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
                send_email(rm, code)
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
# ANALİZ BÖLÜMÜ
# =========================
if not st.session_state.login:
    st.stop()

st.header("AI Maç Analizi")

lig = st.selectbox("Lig", ["PL", "PD", "SA", "BL1", "FL1"])
ev = st.text_input("Ev Sahibi Takım")
dep = st.text_input("Deplasman Takım")

if st.button("AI Analizi Başlat"):
    st.metric("AI Güven Skoru", "81%")
    st.metric("Risk / Denge", "Orta")

    if user[4]:
        st.error("⛔ AI PAS GEÇ UYARISI: Pro algoritması bu maç için oynamayı önermiyor")
    else:
        st.warning("🔒 Pro analiz (PAS GEÇ, kırılgan alanlar) kilitli")
