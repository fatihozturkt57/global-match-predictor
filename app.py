import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime

st.set_page_config(page_title="Demo Finans Platformu", layout="wide")
st.title("💰 Kişisel Finans Yönetimi - Demo")

# ------------------------
# Kullanıcı Sistemi
# ------------------------
if "users" not in st.session_state:
    st.session_state.users = {"admin": "admin123"}  # demo admin
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı")
    password = st.text_input("Şifre", type="password")
    if st.button("Giriş"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldiniz {username}")
        else:
            st.error("Kullanıcı adı veya şifre yanlış.")

def register():
    st.subheader("Kayıt Ol")
    new_user = st.text_input("Yeni Kullanıcı Adı", key="reg_user")
    new_pass = st.text_input("Yeni Şifre", type="password", key="reg_pass")
    if st.button("Kayıt Ol"):
        if new_user in st.session_state.users:
            st.error("Bu kullanıcı adı zaten var.")
        elif new_user.strip() == "" or new_pass.strip() == "":
            st.error("Lütfen geçerli bilgiler girin.")
        else:
            st.session_state.users[new_user] = new_pass
            st.success("Kayıt başarılı! Artık giriş yapabilirsiniz.")

if not st.session_state.logged_in:
    col1, col2 = st.columns(2)
    with col1:
        login()
    with col2:
        register()
else:
    st.success(f"Giriş yapıldı: {st.session_state.username}")

    # ------------------------
    # Kullanıcı Verileri
    # ------------------------
    if "data" not in st.session_state:
        st.session_state.data = pd.DataFrame(columns=["Tarih", "Kategori", "Açıklama", "Tutar"])

    st.subheader("Gelir / Gider Ekle")
    with st.form("veri_form"):
        tarih = st.date_input("Tarih", datetime.date.today())
        kategori = st.selectbox("Kategori", ["Gelir", "Gıda", "Ulaşım", "Fatura", "Diğer"])
        aciklama = st.text_input("Açıklama")
        tutar = st.number_input("Tutar (₺)", min_value=0.0, step=0.01)
        submitted = st.form_submit_button("Ekle")
        if submitted:
            st.session_state.data = pd.concat([st.session_state.data, 
                                               pd.DataFrame([[tarih, kategori, aciklama, tutar]],
                                                            columns=["Tarih", "Kategori", "Açıklama", "Tutar"])], ignore_index=True)
            st.success("Veri eklendi!")

    st.subheader("Geçmiş Veriler")
    st.dataframe(st.session_state.data)

    # ------------------------
    # Ücretsiz / Pro Demo
    # ------------------------
    st.divider()
    st.subheader("Pro Demo Özellikler (Ödeme Yok, Demo Modu)")

    # Gelir-Gider Grafik
    st.write("💹 Kategori Bazlı Harcama Dağılımı")
    if not st.session_state.data.empty:
        cat_data = st.session_state.data.groupby("Kategori")["Tutar"].sum()
        fig, ax = plt.subplots()
        ax.pie(cat_data, labels=cat_data.index, autopct="%1.1f%%")
        st.pyplot(fig)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # Basit Trend Grafiği
    st.write("📈 Zaman Bazlı Harcama / Gelir Trendleri")
    if not st.session_state.data.empty:
        trend_data = st.session_state.data.groupby("Tarih")["Tutar"].sum()
        fig2, ax2 = plt.subplots()
        ax2.plot(trend_data.index, trend_data.values, marker="o")
        ax2.set_xlabel("Tarih")
        ax2.set_ylabel("Toplam Tutar (₺)")
        st.pyplot(fig2)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # PDF Rapor (Demo)
    st.write("📄 PDF Rapor (Demo)")
    st.download_button("Raporu İndir (Demo)", "Bu bir demo PDF raporudur.", file_name="rapor_demo.txt")
