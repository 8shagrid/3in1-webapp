import streamlit as st
from streamlit_extras.dataframe_explorer import dataframe_explorer
from data_manager import load_data


def show_home():
    st.subheader("Selamat Datang, di Website Aplikasi Analisis Barokah Simbok")
    st.write("")
    st.write("")
    st.write("")

    col1, col2 = st.columns(2)
    with col1:
        # Gambar visual atau elemen grafik yang menarik
        st.image("images/pexels-anna-nekrashevich-6801648.jpg", use_container_width=True)

    with col2:
        st.write("")
        st.markdown("### 3 in 1!")
        st.markdown(
            "Aplikasi ini memberikan fitur - fitur yang sangat berguna untuk menganalisis data dan memprediksi churn pelanggan. "
            "Dengan fitur-fitur seperti Advanced Analysis dan Churn Prediction, Anda dapat mengambil keputusan bisnis yang lebih baik. "
            "Gunakan sidebar di sebelah kiri untuk menjelajahi fungsionalitas yang disediakan."
        )

        st.write("")
        st.write("")
        st.write("")

        # Poin-fitur yang menyoroti fitur-fitur utama
        st.markdown("### Fitur Utama:")
        st.write(
            "- **Dashboard Visualisasi**: Menampilkan data dalam bentuk grafik dan plot yang interaktif dan informatif."
        )
        st.write(
            "- **Advanced Analysis**: Jelajahi dan analisis data menggunakan Pygwalker."
        )
        st.write(
            "- **Churn Prediction**: Prediksi churn pelanggan berdasarkan fitur yang dimasukkan."
        )

        st.write("")
        st.write("")
        st.write("")

        # Pewarnaan dan tampilan desain yang menarik
        st.markdown("### Mari Mulai Menganalisis Data Anda!")
        # Gunakan pewarnaan yang sesuai dengan tema situs Anda
