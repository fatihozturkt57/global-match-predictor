import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Demo Finans Platformu", layout="wide")
st.title("💰 Kişisel Finans Yönetimi - Demo Pro Gelişmiş")

# ------------------------
# Kullanıcı Sistemi
# ------------------------
if "users" not in st.session_state:
    st.session_state.users = {"fatih": "575757", "admin": "admin123"}  # hazır admin
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Tarih", "Kategori", "Açıklama", "Tutar"])

def login():
    st.subheader("Giriş Yap")
    login_user = st.text_input("Kullanıcı Adı", key="login_user_field")
    login_pass = st.text_input("Şifre", type="password", key="login_pass_field")
    if st.button("Giriş", key="login_button"):
        users = st.session_state.users
        if login_user in users and users[login_user] == login_pass:
            st.session_state.logged_in = True
            st.session_state.username = login_user
            st.success(f"Hoşgeldiniz {login_user}")
        else:
            st.error("Kullanıcı adı veya şifre yanlış.")

def register():
    st.subheader("Kayıt Ol")
    reg_user = st.text_input("Yeni Kullanıcı Adı", key="reg_user_field")
    reg_pass = st.text_input("Yeni Şifre", type="password", key="reg_pass_field")
    if st.button("Kayıt Ol", key="reg_button"):
        if reg_user.strip() == "" or reg_pass.strip() == "":
            st.error("Lütfen geçerli bilgiler girin.")
        elif reg_user in st.session_state.users:
            st.error("Bu kullanıcı adı zaten var.")
        else:
            st.session_state.users[reg_user] = reg_pass
            st.success("Kayıt başarılı! Artık giriş yapabilirsiniz.")

# ------------------------
# Giriş / Kayıt Kontrolü
# ------------------------
if not st.session_state.logged_in:
    col1, col2 = st.columns(2)
    with col1:
        login()
    with col2:
        register()
else:
    st.success(f"Giriş yapıldı: {st.session_state.username}")
    st.write("Demo verilerinizi buradan yönetebilirsiniz...")
