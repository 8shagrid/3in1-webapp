import pandas as pd
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.dataframe_explorer import dataframe_explorer
from data_manager import load_data


def show_dashboard():
    st.header("Dashboard")

    # Filter Data
    filtered_df = dataframe_explorer(
        load_data(),
        case=False,
    )

    st.markdown("""---""")

    # horizontal menu
    selected = option_menu(
        None,
        ["Customer Data Analysis", "Customer Churn Analysis"],
        icons=["clipboard2-data-fill", "sign-stop"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
    )
    st.markdown("""---""")

    if selected == "Customer Data Analysis":
        display_customer_data_analysis(filtered_df)
    elif selected == "Customer Churn Analysis":
        display_churn_analysis(filtered_df)


def display_customer_data_analysis(filtered_df):
    ### __BARIS KE-1__ ###
    col1, col2, col3 = st.columns(3)

    with col1:
        # Menghitung jumlah seluruh pelanggan
        total_customers = filtered_df["Customer ID"].count()
        st.markdown("#### Total Customers")
        st.markdown(f"# {total_customers}")

    with col2:
        # Menghitung jumlah pelanggan yang churn (Churn Label = 'Yes')
        churned_customers = filtered_df[filtered_df["Churn Label"] == "Yes"][
            "Customer ID"
        ].count()
        # Menghitung total jumlah pelanggan
        total_customers = filtered_df["Customer ID"].count()
        # Menghitung churn rate
        churn_rate = (churned_customers / total_customers) * 100

        st.markdown("#### Customer Churn Rate")
        st.markdown(f"# {churn_rate:.2f}%")

    with col3:
        # Menghitung rata-rata customer tenure (Tenure Months)
        average_tenure = filtered_df["Tenure Months"].mean()

        st.write("#### Average Customer Tenure")
        st.markdown(f"# {average_tenure:.0f} months")

    st.markdown("""---""")

    ### __BARIS KE-2__ ###
    col4, col5 = st.columns([2, 1])

    with col4:
        st.markdown("#### Customer Location Map")
        # Peta Lokasi
        fig = px.scatter_mapbox(
            filtered_df.groupby(["Latitude", "Longitude"])["Customer ID"]
            .count()
            .reset_index(),
            lat="Latitude",
            lon="Longitude",
            hover_data=["Customer ID"],
            zoom=8,
            color_discrete_sequence=["navy"],
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    with col5:
        st.markdown("#### Location Distribution of Customers")
        # Menghitung jumlah masing-masing lokasi
        location_counts = filtered_df["Location"].value_counts().reset_index()
        location_counts.columns = ["Location", "Count"]

        # Membuat Bar Chart menggunakan Plotly Express
        fig = px.bar(
            location_counts,
            x="Location",
            y="Count",
            labels={"Count": "Number of Customers"},
            color="Location",
            text="Count",
        )
        fig.update_layout(
            xaxis_title="Location",
            yaxis_title="Number of Customers",
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    ### __BARIS KE-3__ ###
    col6, col7, col8 = st.columns(3)

    with col6:
        st.markdown("#### Device Class Distribution of Customers")
        # Menghitung jumlah masing-masing kelas perangkat
        device_class_counts = filtered_df["Device Class"].value_counts().reset_index()
        device_class_counts.columns = ["Device Class", "Count"]

        # Membuat Pie Chart menggunakan Plotly Express
        fig = px.pie(
            device_class_counts,
            names="Device Class",
            values="Count",
            hole=0.4,
            labels={"Count": "Number of Customers"},
        )

        # Menampilkan grafik
        st.plotly_chart(fig, use_container_width=True)

    with col7:
        st.markdown("#### Payment Method Distribution of Customers")
        # Menghitung jumlah masing-masing metode pembayaran
        payment_method_counts = (
            filtered_df["Payment Method"].value_counts().reset_index()
        )
        payment_method_counts.columns = ["Payment Method", "Count"]

        # Membuat Bar Chart menggunakan Plotly Express
        fig = px.bar(
            payment_method_counts,
            x="Payment Method",
            y="Count",
            labels={"Count": "Number of Customers"},
            color="Payment Method",
            text="Count",
        )
        fig.update_layout(
            xaxis_title="Payment Method",
            yaxis_title="Number of Customers",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col8:
        st.markdown("#### Service Usage")
        # Buat dropdown untuk memilih layanan
        selected_service = st.selectbox(
            "Select a Service",
            [
                "Games Product",
                "Music Product",
                "Education Product",
                "Video Product",
                "Use MyApp",
                "Call Center",
            ],
        )

        # Mendapatkan data berdasarkan layanan yang dipilih
        if selected_service == "Games Product":
            service_column = "Games Product"
        elif selected_service == "Music Product":
            service_column = "Music Product"
        elif selected_service == "Education Product":
            service_column = "Education Product"
        elif selected_service == "Video Product":
            service_column = "Video Product"
        elif selected_service == "Use MyApp":
            service_column = "Use MyApp"
        elif selected_service == "Call Center":
            service_column = "Call Center"

        # Menghitung frekuensi penggunaan layanan yang dipilih
        service_counts = filtered_df[service_column].value_counts()

        # Membuat dataframe baru dengan hasil perhitungan
        usage_data = {
            selected_service: service_counts.index,
            "Count": service_counts.values,
        }
        usage_df = pd.DataFrame(usage_data)

        # Membuat grafik pie
        fig = px.pie(
            usage_df,
            names=selected_service,
            values="Count",
            hole=0.4,
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    ### __BARIS KE-4__ ###
    col9, col10 = st.columns(2)
    with col9:
        st.markdown("#### Monthly Purchase (Thou. IDR) Distribution")
        fig = px.histogram(
            filtered_df,
            x="Monthly Purchase (Thou. IDR)",
            nbins=20,
        )
        fig.update_xaxes(title_text="Monthly Purchase (Thou. IDR)")
        fig.update_yaxes(title_text="Number of Customers")

        st.plotly_chart(fig, use_container_width=True)

    with col10:
        st.markdown("#### CLTV (Predicted Thou. IDR) Distribution")
        fig = px.histogram(
            filtered_df,
            x="CLTV (Predicted Thou. IDR)",
            nbins=20,
        )
        fig.update_xaxes(title_text="CLTV (Predicted Thou. IDR)")
        fig.update_yaxes(title_text="Number of Customers")

        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    ### __BARIS KE-5__ ###
    col11, col12 = st.columns(2)
    with col11:
        st.markdown("#### Heatmap Analysis")
        # Dropdown for selecting columns
        columns = [
            "Tenure Months",
            "Monthly Purchase (Thou. IDR)",
            "CLTV (Predicted Thou. IDR)",
        ]

        selected_columns = st.multiselect(
            "Select columns for correlation analysis", columns, default=columns
        )

        if selected_columns:
            # Calculate correlation matrix for selected columns
            correlation_matrix = filtered_df[selected_columns].corr()

            # Create a correlation heatmap using Plotly
            fig = px.imshow(
                correlation_matrix,
                x=selected_columns,
                y=selected_columns,
                color_continuous_scale="Viridis",
            )

            # Customize the heatmap layout
            fig.update_layout(
                xaxis_title="Features",
                yaxis_title="Features",
                coloraxis_colorbar=dict(title="Correlation"),
            )

            # Display the heatmap
            st.plotly_chart(fig)
        else:
            st.warning("Please select at least one column for correlation analysis.")

    with col12:
        st.markdown("#### Scatter Plot Analysis")
        # Dropdown for selecting x and y columns
        columns = [
            "Tenure Months",
            "Monthly Purchase (Thou. IDR)",
            "CLTV (Predicted Thou. IDR)",
        ]

        x_column = st.selectbox(
            "Select X-axis column",
            options=columns,
            index=0,
        )
        y_column = st.selectbox(
            "Select Y-axis column",
            options=columns,
            index=1,
        )

        if x_column != y_column:
            # Create a scatter plot using Plotly Express
            scatter_fig = px.scatter(
                filtered_df,
                x=x_column,
                y=y_column,
            )

            # Customize the scatter plot layout
            scatter_fig.update_layout(
                xaxis_title=x_column,
                yaxis_title=y_column,
            )

            # Display the scatter plot
            st.plotly_chart(scatter_fig)
        else:
            st.warning("Please select different columns for X and Y axes.")

    st.markdown("""---""")

    ### __BARIS KE-6__ ###
    st.markdown("#### Filtered Data Frame")
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown("""---""")


def display_churn_analysis(filtered_df):
    ### __BARIS KE-1__ ###
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        # Menghitung jumlah pelanggan yang churn (Churn Label = 'Yes')
        churned_customers = filtered_df[filtered_df["Churn Label"] == "Yes"][
            "Customer ID"
        ].count()
        st.markdown("#### Total Customers Churn")
        st.markdown(f"## {churned_customers}")

    with col2:
        # Menghitung jumlah pelanggan yang churn (Churn Label = 'Yes')
        churned_customers = filtered_df[filtered_df["Churn Label"] == "Yes"][
            "Customer ID"
        ].count()
        # Menghitung total jumlah pelanggan
        total_customers = filtered_df["Customer ID"].count()
        # Menghitung churn rate
        churn_rate = (churned_customers / total_customers) * 100

        st.markdown("#### Customer Churn Rate")
        st.markdown(f"## {churn_rate:.2f}%")

    with col3:
        # Filter data hanya untuk pelanggan dengan label churn "Yes"
        churned_customers = filtered_df[filtered_df["Churn Label"] == "Yes"]

        # Hitung rata-rata pembelian bulanan
        average_monthly_purchase = churned_customers[
            "Monthly Purchase (Thou. IDR)"
        ].mean()
        st.write("#### Average Monthly Purchase Churn")
        st.markdown(f"## {average_monthly_purchase:.2f} Thou. IDR")

    with col4:
        # Filter data hanya untuk pelanggan dengan label churn "Yes"
        churned_customers = filtered_df[filtered_df["Churn Label"] == "Yes"]

        sum_monthly_purchase = churned_customers["Monthly Purchase (Thou. IDR)"].sum()

        st.write("#### Total Monthly Purchase Churn")
        st.markdown(f"## {sum_monthly_purchase:.2f} Thou. IDR")

    st.markdown("""---""")

    col5, col6 = st.columns(2)

    with col5:
        # Membuat kolom baru 'Churn' sebagai contoh (sesuaikan dengan dataset Anda)
        filtered_df["Churn"] = filtered_df["Churn Label"] == "Yes"

        # Membuat Pie Chart
        churn_count = filtered_df["Churn"].value_counts()
        fig = px.pie(
            names=["Churn", "Non-Churn"],
            values=churn_count,
            hole=0.5,
            title="Churn vs. Non-Churn Customers",
        )
        st.plotly_chart(fig, use_container_width=True)

    with col6:
        # Filter data berdasarkan Churn Label
        churn_data = filtered_df[filtered_df["Churn Label"] == "Yes"]

        # Group data berdasarkan Tenure Months
        churn_by_tenure = (
            churn_data.groupby("Tenure Months").size().reset_index(name="Count")
        )

        # Buat Bar Chart menggunakan Plotly Express
        fig = px.bar(
            churn_by_tenure,
            x="Tenure Months",
            y="Count",
            title="Churn by Tenure Months",
        )
        fig.update_layout(xaxis_title="Tenure Months", yaxis_title="Count")

        # Tampilkan grafik di Streamlit
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("""---""")

    # Buat dropdown untuk memilih kolom
    selected_service = st.selectbox(
        "Select a Column",
        [
            "Location",
            "Payment Method",
            "Device Class",
            "Games Product",
            "Music Product",
            "Education Product",
            "Video Product",
            "Use MyApp",
            "Call Center",
        ],
    )

    # Mendapatkan data berdasarkan kolom yang dipilih
    if selected_service == "Location":
        service_column = "Location"
    if selected_service == "Payment Method":
        service_column = "Payment Method"
    if selected_service == "Device Class":
        service_column = "Device Class"
    elif selected_service == "Games Product":
        service_column = "Games Product"
    elif selected_service == "Music Product":
        service_column = "Music Product"
    elif selected_service == "Education Product":
        service_column = "Education Product"
    elif selected_service == "Video Product":
        service_column = "Video Product"
    elif selected_service == "Use MyApp":
        service_column = "Use MyApp"
    elif selected_service == "Call Center":
        service_column = "Call Center"

    col_fig_0, col_fig_1, col_fig_2 = st.columns(3)

    with col_fig_0:
        st.markdown(f"#### Total Customer by {selected_service}")
        # Membuat grafik pie
        fig0 = px.bar(
            filtered_df.groupby(selected_service)["Customer ID"].count().reset_index(),
            x=selected_service,
            y="Customer ID",
            color=selected_service,
            text="Customer ID",
        )
        st.plotly_chart(fig0, use_container_width=True)

    with col_fig_1:
        # st.markdown(f"#### Churn Rate by {selected_service}")
        # fig0 = px.pie(
        #     filtered_df.groupby([selected_service, "Churn Label"])["Customer ID"]
        #     .count()
        #     .reset_index(),
        #     values="Customer ID",
        #     facet_col="Churn Label",
        #     hole=0.5,
        #     names=selected_service,
        # )
        # st.plotly_chart(fig0, use_container_width=True)

        # Membuat tabel kontingensi antara Layanan dan 'Churn Label'
        contingency_table = pd.crosstab(
            filtered_df[selected_service], filtered_df["Churn Label"]
        )

        # Hitung proporsi Churn (pemutusan hubungan) untuk setiap Layanan
        contingency_table["Churn Rate"] = (
            contingency_table["Yes"]
            / (contingency_table["Yes"] + contingency_table["No"])
        ) * 100

        # Plotting menggunakan Plotly Pie Chart
        fig1 = px.pie(
            contingency_table,
            names=contingency_table.index,
            values="Churn Rate",
            title=f"Churn Rate by {selected_service}",
            labels={"Churn Rate": "Churn Rate (%)", "index": selected_service},
            hole=0.3,
        )

        # Menambahkan label pada setiap sektor pie
        fig1.update_traces(textinfo="percent+label", pull=[0.1, 0.1, 0.1, 0.1])
        st.plotly_chart(fig1, use_container_width=True)

    with col_fig_2:
        st.markdown(f"#### Total Churn by {selected_service} and Churn Label")

        fig2 = px.bar(
            filtered_df.groupby([selected_service, "Churn Label"])["Customer ID"]
            .count()
            .reset_index(),
            x=selected_service,
            y="Customer ID",
            color="Churn Label",
            barmode="group",
            text="Customer ID",
        )

        # Menampilkan grafik menggunakan Streamlit
        st.plotly_chart(fig2, use_container_width=True)

    col_fig_3, col_fig_4 = st.columns(2)

    with col_fig_3:
        st.markdown(f"#### Average Monthly Purchase by {selected_service}")
        device_class = (
            filtered_df.groupby(selected_service)["Monthly Purchase (Thou. IDR)"]
            .mean()
            .reset_index()
        )

        # Membuat plot
        fig3 = px.bar(
            device_class,
            x=selected_service,
            y="Monthly Purchase (Thou. IDR)",
            color=selected_service,
            labels="Monthly Purchase (Thou. IDR)",
        )

        # Mengatur format angka dengan dua angka di belakang koma
        fig3.update_traces(texttemplate="%{y:.2f}", textposition="inside")
        st.plotly_chart(fig3, use_container_width=True)

    with col_fig_4:
        st.markdown(
            f"#### Average Monthly Purchase by {selected_service} and Churn Label"
        )
        device_class_churn = (
            filtered_df.groupby([selected_service, "Churn Label"])[
                "Monthly Purchase (Thou. IDR)"
            ]
            .mean()
            .reset_index()
        )

        # Membuat plot
        fig4 = px.bar(
            device_class_churn,
            x=selected_service,
            y="Monthly Purchase (Thou. IDR)",
            color="Churn Label",
            barmode="group",
            labels="Monthly Purchase (Thou. IDR)",
        )

        # Mengatur format angka dengan dua angka di belakang koma
        fig4.update_traces(texttemplate="%{y:.2f}", textposition="inside")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("""---""")
    st.markdown("#### Filtered Data Frame")
    st.dataframe(filtered_df, use_container_width=True)
    st.markdown("""---""")
