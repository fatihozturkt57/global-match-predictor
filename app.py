import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="Demo Finans Platformu", layout="wide")

st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>💰 Kişisel Finans Yönetimi - Pro Demo</h1>
    """, unsafe_allow_html=True
)

# ------------------------
# Kullanıcı Sistemi
# ------------------------
if "users" not in st.session_state:
    st.session_state.users = {"fatih": "575757", "admin": "admin123"}
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Tarih", "Kategori", "Açıklama", "Tutar"])
if "pro_active" not in st.session_state:
    st.session_state.pro_active = False

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

    # ------------------------
    # Gelir / Gider Ekleme
    # ------------------------
    st.subheader("💸 Gelir / Gider Ekle")
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
    # Veri Tablosu
    # ------------------------
    st.subheader("📊 Verileriniz")
    st.dataframe(st.session_state.data)

    # ------------------------
    # Özet Kartlar
    # ------------------------
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

    # ------------------------
    # Kategori Bazlı Harcama Grafiği
    # ------------------------
    st.subheader("💹 Kategori Bazlı Harcama Dağılımı")
    if not st.session_state.data.empty:
        cat_data = st.session_state.data.groupby("Kategori")["Tutar"].sum()
        st.bar_chart(cat_data)

    # ------------------------
    # Trend Grafiği
    # ------------------------
    st.subheader("📈 Zaman Bazlı Harcama / Gelir Trendleri")
    if not st.session_state.data.empty:
        trend_data = st.session_state.data.groupby("Tarih")["Tutar"].sum()
        st.line_chart(trend_data)

    # ------------------------
    # Pro Demo Butonu
    # ------------------------
    st.subheader("💎 Pro Demo Özellikleri")
    if st.button("Pro Demo Aç"):
        st.session_state.pro_active = True
        st.success("🎉 Pro demo özellikleri aktif!")

    # ------------------------
    # Pro Analizler
    # ------------------------
    if st.session_state.pro_active and not st.session_state.data.empty:
        st.subheader("🧠 Pro Analiz & Öneriler")
        last_7_days = st.session_state.data[st.session_state.data["Tarih"] >= (datetime.date.today() - datetime.timedelta(days=7))]
        last_30_days = st.session_state.data[st.session_state.data["Tarih"] >= (datetime.date.today() - datetime.timedelta(days=30))]

        income_7 = last_7_days[last_7_days["Kategori"]=="Gelir"]["Tutar"].sum()
        expense_7 = last_7_days[last_7_days["Kategori"]!="Gelir"]["Tutar"].sum()
        income_30 = last_30_days[last_30_days["Kategori"]=="Gelir"]["Tutar"].sum()
        expense_30 = last_30_days[last_30_days["Kategori"]!="Gelir"]["Tutar"].sum()

        # Mini Finansal Sağlık Skoru
        score = max(0, min(100, int((income_30 - expense_30)/(income_30+1)*100)))
        st.metric("Finansal Sağlık Skoru (0-100)", score)

        # Akıllı Öneriler
        if expense_7 > income_7:
            st.warning("⚠ Son 7 gün giderleriniz gelirlerinizden fazla!")
        else:
            st.success("✅ Son 7 gün dengeli mali durum.")

        if expense_30 > income_30:
            st.warning("⚠ Son 30 gün giderleriniz gelirlerinizden fazla!")
        else:
            st.success("✅ Son 30 gün dengeli mali durum.")

        # Kategori bazlı en yüksek harcama uyarısı
        if not last_30_days[last_30_days["Kategori"]!="Gelir"].empty:
            high_cat = last_30_days[last_30_days["Kategori"]!="Gelir"].groupby("Kategori")["Tutar"].sum().idxmax()
            st.info(f"💡 Son 30 günün en yüksek harcama kategorisi: {high_cat}")
