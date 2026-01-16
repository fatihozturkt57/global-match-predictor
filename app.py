if st.button("🧠 AI ANALİZİNİ BAŞLAT"):
        e, d = veriler[ev_adi], veriler[dep_adi]
        
        # Oynanan maç sayılarını güvenli alalım (0'a bölme hatası için)
        e_mac = e.get('playedGames', 1)
        d_mac = d.get('playedGames', 1)
        
        # 1. TEMEL İSTATİSTİKLER (Hücum ve Savunma Gücü)
        e_at = e['goalsFor'] / e_mac
        e_ye = e['goalsAgainst'] / e_mac
        d_at = d['goalsFor'] / d_mac
        d_ye = d['goalsAgainst'] / d_mac

        # 2. SKOR TAHMİNİ (Gerçekçi Yuvarlama)
        # Evin atacağı: (Kendi hücumu + Rakip defans zafiyeti) / 2
        e_xg = (e_at + d_ye) / 2 + 0.2
        d_xg = (d_at + e_ye) / 2
        
        final_ev = round(e_xg)
        final_dep = round(d_xg)

        # --- SONUÇLARI EKRANA BASAN KISIM ---
        st.divider()
        st.subheader(f"🏟️ {ev_adi} vs {dep_adi} Analiz Raporu")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Tahmini Skor", f"{final_ev} - {final_dep}")
        m2.metric("İY Tahmini", f"{1 if e_xg > 1.8 else 0} - {1 if d_xg > 2.0 else 0}")
        m3.metric("Tahmini Korner", f"{round(7.5 + (e_at + d_at) * 1.5)}+")
        m4.metric("Tahmini
