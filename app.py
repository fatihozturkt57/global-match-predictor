import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Demo Finans Platformu", layout="wide")
st.title("💰 Kişisel Finans Yönetimi - Demo")

# ------------------------
# Kullanıcı Sistemi
# ------------------------
if "users" not in st.session_state:
    st.session_state.users = {"fatih": "575757", "admin": "admin123"}  # özel giriş
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı", key="login_user")
    password = st.text_input("Şifre", type="password", key="login_pass")
    if st.button("Giriş", key="login_btn"):
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
    if st.button("Kayıt Ol", key="reg_btn"):
        if new_user in st.session_state.users:
            st.error("Bu kullanıcı adı zaten var.")
        elif new_user.strip() == "" or new_pass.strip() == "":
            st.error("Lütfen geçerli bilgiler girin.")
        else:
            st.session_state.users[new_user] = new_pass
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

    # Kategori Bazlı Harcama
    st.write("💹 Kategori Bazlı Harcama Dağılımı")
    if not st.session_state.data.empty:
        cat_data = st.session_state.data.groupby("Kategori")["Tutar"].sum()
        st.bar_chart(cat_data)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # Trend Grafiği
    st.write("📈 Zaman Bazlı Harcama / Gelir Trendleri")
    if not st.session_state.data.empty:
        trend_data = st.session_state.data.groupby("Tarih")["Tutar"].sum()
        st.line_chart(trend_data)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # ------------------------
    # Mini Akıllı Öneriler (Pro Demo)
    # ------------------------
    st.write("🧠 Mini Akıllı Öneriler (Pro Demo)")

    if not st.session_state.data.empty:
        toplam_gider = st.session_state.data[st.session_state.data["Kategori"] != "Gelir"]["Tutar"].sum()
        toplam_gelir = st.session_state.data[st.session_state.data["Kategori"] == "Gelir"]["Tutar"].sum()
        fark = toplam_gelir - toplam_gider

        if fark > 0:
            st.success(f"💡 Gelirler giderlerden {fark:.2f}₺ fazla, mali durum pozitif.")
        elif fark < 0:
            st.warning(f"⚠️ Giderler gelirlerden {-fark:.2f}₺ fazla, dikkatli olun!")
        else:
            st.info("💡 Gelir ve giderleriniz dengede.")

        # Son 7 gün trend kontrolü
        son_veri = st.session_state.data.tail(7)
        if not son_veri.empty:
            son_toplam = son_veri["Tutar"].sum()
            st.info(f"📊 Son 7 gün toplam hareket: {son_toplam:.2f}₺")

    # PDF Rapor (Demo)
    st.write("📄 PDF Rapor (Demo)")
    st.download_button("Raporu İndir (Demo)", "Bu bir demo PDF raporudur.", file_name="rapor_demo.txt")
