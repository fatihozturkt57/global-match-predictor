import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Demo Finans Platformu", layout="wide")
st.title("💰 Kişisel Finans Yönetimi - Demo Pro Gelişmiş")

# ------------------------
# Kullanıcı Sistemi
# ------------------------
if "users" not in st.session_state:
    st.session_state.users = {"fatih": "575757", "admin": "admin123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def login():
    st.subheader("Giriş Yap")
    username = st.text_input("Kullanıcı Adı", key="login_user_unique")
    password = st.text_input("Şifre", type="password", key="login_pass_unique")
    if st.button("Giriş", key="login_btn_unique"):
        if username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"Hoşgeldiniz {username}")
        else:
            st.error("Kullanıcı adı veya şifre yanlış.")

def register():
    st.subheader("Kayıt Ol")
    new_user = st.text_input("Yeni Kullanıcı Adı", key="reg_user_unique")
    new_pass = st.text_input("Yeni Şifre", type="password", key="reg_pass_unique")
    if st.button("Kayıt Ol", key="reg_btn_unique"):
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

    # ------------------------
    # Free / Pro Demo Dashboard
    # ------------------------
    st.subheader("Geçmiş Veriler")
    st.dataframe(st.session_state.data)

    st.divider()
    st.subheader("Pro Demo Özellikler (Ödeme Yok, Demo Modu)")

    # Hızlı Özet Kartları
    if not st.session_state.data.empty:
        total_income = st.session_state.data[st.session_state.data["Kategori"] == "Gelir"]["Tutar"].sum()
        total_expense = st.session_state.data[st.session_state.data["Kategori"] != "Gelir"]["Tutar"].sum()
        balance = total_income - total_expense
        max_cat = st.session_state.data[st.session_state.data["Kategori"] != "Gelir"].groupby("Kategori")["Tutar"].sum().idxmax() \
            if not st.session_state.data[st.session_state.data["Kategori"] != "Gelir"].empty else "Yok"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Toplam Gelir", f"{total_income:.2f}₺")
        c2.metric("Toplam Gider", f"{total_expense:.2f}₺")
        c3.metric("Kalan Bütçe", f"{balance:.2f}₺")
        c4.metric("En Yüksek Harcama", max_cat)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # ------------------------
    # Kategori Bazlı Harcama Grafikleri
    # ------------------------
    st.write("💹 Kategori Bazlı Harcama Dağılımı (Pro Demo)")
    if not st.session_state.data.empty:
        cat_data = st.session_state.data.groupby("Kategori")["Tutar"].sum()
        fig, ax = plt.subplots()
        ax.pie(cat_data, labels=cat_data.index, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        st.pyplot(fig)
    else:
        st.info("Henüz veri yok. Gelir veya gider ekleyin.")

    # ------------------------
    # Trend Grafiği
    # ------------------------
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
        fark = total_income - total_expense
        if fark > 0:
            st.success(f"💡 Gelirler giderlerden {fark:.2f}₺ fazla, mali durum pozitif.")
        elif fark < 0:
            st.warning(f"⚠️ Giderler gelirlerden {-fark:.2f}₺ fazla, dikkatli olun!")
        else:
            st.info("💡 Gelir ve giderleriniz dengede.")

        # Son 7 gün trend
        son_veri = st.session_state.data.tail(7)
        if not son_veri.empty:
            son_toplam = son_veri["Tutar"].sum()
            st.info(f"📊 Son 7 gün toplam hareket: {son_toplam:.2f}₺")

        # Kategoriye göre mini uyarılar
        harcama_kat = st.session_state.data[st.session_state.data["Kategori"] != "Gelir"].groupby("Kategori")["Tutar"].sum()
        for k, v in harcama_kat.items():
            if v > 500:  # demo threshold
                st.warning(f"⚠️ {k} harcamaları yüksek: {v:.2f}₺")
            else:
                st.info(f"✅ {k} harcamaları normal: {v:.2f}₺")

        # Mini ek özellik: Son 3 gün harcama trendi
        son3 = st.session_state.data.tail(3)
        if not son3.empty:
            st.info(f"📈 Son 3 gün harcama trendi toplam: {son3['Tutar'].sum():.2f}₺")

    # PDF Rapor (Demo)
    st.write("📄 PDF Rapor (Demo)")
    st.download_button("Raporu İndir (Demo)", "Bu bir demo PDF raporudur.", file_name="rapor_demo.txt")

    # Demo Pas Geç Uyarısı
    if st.session_state.data.empty:
        st.error("⛔ Demo için yeterli veri yok. Lütfen birkaç gelir/gider girin.")
