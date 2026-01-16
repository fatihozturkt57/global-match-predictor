import streamlit as st
import requests
import random
import sqlite3
import smtplib
from email.mime.text import MIMEText
from twilio.rest import Client

# =========================
# AYARLAR (DOLDUR)
# =========================
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_EMAIL = "YOUR_EMAIL@gmail.com"
SMTP_PASSWORD = "APP_PASSWORD"

TWILIO_SID = "TWILIO_SID"
TWILIO_TOKEN = "TWILIO_TOKEN"
TWILIO_PHONE = "+123456789"

API_KEY = "FOOTBALL_API_KEY"
HEADERS = {"X-Auth-Token": API_KEY}

# =========================
# DB
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
# YARDIMCI FONKSİYONLAR
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

def send_sms(to, code):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        body=f"AI doğrulama kodunuz: {code}",
        from_=TWILIO_PHONE,
        to=to
    )

def get_user(username):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def make_pro(username):
    c.execute("UPDATE users SET pro=1 WHERE username=?", (username,))
    conn.commit()

# =========================
# STREAMLIT
# =========================
st.set_page_config("AI Pro Predictor", layout="wide")
st.title("AI Futbol Analiz Platformu")

if "login" not in st.session_state:
    st.session_state.login = None

# =========================
# AUTH
# =========================
with st.sidebar:
    if not st.session_state.login:
        tab1, tab2 = st.tabs(["Giriş", "Kayıt"])

        with tab1:
            u = st.text_input("Kullanıcı")
            p = st.text_input("Şifre", type="password")
            if st.button("Giriş"):
                user = get_user(u)
                if user and user[1] == p:
                    st.session_state.login = u
                    st.rerun()
                else:
                    st.error("Hatalı giriş")

        with tab2:
            ru = st.text_input("Kullanıcı Adı", key="ru")
            rm = st.text_input("E-posta", key="rm")
            rp = st.text_input("Telefon (+90...)", key="rp")
            rpw = st.text_input("Şifre", type="password", key="rpw")

            if st.button("Kod Gönder"):
                code = random.randint(100000, 999999)
                st.session_state.code = code
                send_email(rm, code)
                send_sms(rp, code)
                st.success("Kod gönderildi")

            rc = st.text_input("Doğrulama Kodu")

            if st.button("Kayıt Ol"):
                if int(rc) == st.session_state.code:
                    c.execute(
                        "INSERT INTO users VALUES (?,?,?,?,0,1)",
                        (ru, rpw, rm, rp)
                    )
                    conn.commit()
                    st.success("Kayıt başarılı")
                else:
                    st.error("Kod yanlış")

    else:
        user = get_user(st.session_state.login)
        st.success(f"Hoş geldin {user[0]}")
        if user[4]:
            st.success("🔥 PRO AKTİF")
        else:
            st.warning("FREE ÜYELİK")

            if st.button("💳 Pro Satın Al (Demo)"):
                make_pro(user[0])
                st.success("Ödeme alındı → Pro aktif")
                st.rerun()

        if st.button("Çıkış"):
            st.session_state.login = None
            st.rerun()

# =========================
# ANALİZ (KISALTTIM)
# =========================
if not st.session_state.login:
    st.stop()

st.header("AI Maç Analizi")

lig = st.selectbox("Lig", ["PL", "PD", "SA"])
ev = st.text_input("Ev Sahibi")
dep = st.text_input("Deplasman")

if st.button("Analiz"):
    st.metric("AI Güven Skoru", "82%")

    if user[4]:
        st.success("⛔ AI PAS GEÇ UYARISI: Pro algoritması aktif")
    else:
        st.info("🔒 Pro analizler kilitli")
