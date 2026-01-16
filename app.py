        st.divider()
    st.subheader("📌 Avantaj / Dezavantaj Nedenleri")

    av_col, dez_col = st.columns(2)

    with av_col:
        st.markdown("### ✅ Avantaj Nedenleri")
        if ev_xg > dep_xg:
            st.write(f"- {ev_adi}, rakibine göre daha yüksek gol beklentisine sahip.")
        if e_h > d_h:
            st.write(f"- {ev_adi}, maç başına daha üretken hücum yapıyor.")
        if e_s < d_s:
