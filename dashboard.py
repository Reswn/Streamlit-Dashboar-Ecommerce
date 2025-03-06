import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# Konfigurasi Halaman
st.set_page_config(page_title="E-Commerce Dashboard", layout="wide")

# Load Data dengan Error Handling
@st.cache_data
def load_data():
    try:
        customers_df = pd.read_csv("customers_dataset.csv")
        orders_df = pd.read_csv("orders_dataset.csv")
        order_payments_df = pd.read_csv("order_payments_dataset.csv")
        order_items_df = pd.read_csv("order_items_dataset.csv")
        return customers_df, orders_df, order_payments_df, order_items_df
    except FileNotFoundError:
        st.error("File dataset tidak ditemukan. Pastikan semua file CSV tersedia.")
        return None, None, None, None

customers_df, orders_df, order_payments_df, order_items_df = load_data()

if customers_df is None or orders_df is None or order_payments_df is None or order_items_df is None:
    st.stop()

# **🔹 Sidebar Navigasi**
st.sidebar.image("Logo.png", width=200)
st.sidebar.title("📊 E-Commerce Dashboard")

# Filter Kalender
st.sidebar.subheader("Filter Tanggal Pesanan")
start_date = st.sidebar.date_input("Dari Tanggal", dt.date(2017, 1, 1))
end_date = st.sidebar.date_input("Sampai Tanggal", dt.date(2018, 12, 31))

# Konversi ke datetime
orders_df["order_purchase_timestamp"] = pd.to_datetime(orders_df["order_purchase_timestamp"])
filtered_orders = orders_df[(orders_df["order_purchase_timestamp"].dt.date >= start_date) & 
                            (orders_df["order_purchase_timestamp"].dt.date <= end_date)]

# Pilihan Analisis
option = st.sidebar.selectbox("Pilih Analisis", [
    "Dashboard Utama",
    "Top 10 Kota dengan Pelanggan Terbanyak",
    "Distribusi Pelanggan per Negara Bagian",
    "Tren Pemesanan dari Waktu ke Waktu",
    "Distribusi Metode Pembayaran",
    "Top 10 Seller dengan Penjualan Terbanyak"
])

# **🔹 Dashboard Utama (Default View)**
if option == "Dashboard Utama":
    st.title("📊 Dashboard E-Commerce Analysis 📊")

    col1, col2 = st.columns(2)

    with col1:
        top_cities = customers_df["customer_city"].value_counts().head(10).reset_index()
        top_cities.columns = ["Kota", "Jumlah Pelanggan"]
        fig1 = px.bar(top_cities, x="Jumlah Pelanggan", y="Kota", orientation="h", 
                      color="Jumlah Pelanggan", color_continuous_scale="Blues",
                      title="Top 10 Kota dengan Pelanggan Terbanyak")
        st.plotly_chart(fig1)

    with col2:
        state_counts = customers_df["customer_state"].value_counts().reset_index()
        state_counts.columns = ["Negara Bagian", "Jumlah Pelanggan"]
        fig2 = px.bar(state_counts, x="Negara Bagian", y="Jumlah Pelanggan", 
                      color="Jumlah Pelanggan", color_continuous_scale="Viridis",
                      title="Distribusi Pelanggan per Negara Bagian")
        st.plotly_chart(fig2)

    # Tren Pemesanan dari Waktu ke Waktu
    filtered_orders["year_month"] = filtered_orders["order_purchase_timestamp"].dt.strftime("%Y-%m")
    orders_trend = filtered_orders.groupby("year_month").size().reset_index()
    orders_trend.columns = ["Bulan", "Jumlah Pesanan"]
    fig3 = px.line(orders_trend, x="Bulan", y="Jumlah Pesanan", markers=True,
                   title="Tren Pemesanan dari Waktu ke Waktu", color_discrete_sequence=["#FF5733"])
    st.plotly_chart(fig3)

    # Distribusi Metode Pembayaran
    payment_counts = order_payments_df["payment_type"].value_counts().reset_index()
    payment_counts.columns = ["Metode Pembayaran", "Jumlah Pengguna"]
    fig4 = px.bar(payment_counts, x="Metode Pembayaran", y="Jumlah Pengguna", 
                  color="Jumlah Pengguna", color_continuous_scale="Viridis",
                  title="Distribusi Metode Pembayaran")
    st.plotly_chart(fig4)

    # Top 10 Seller dengan Penjualan Terbanyak
    top_sellers = order_items_df["seller_id"].value_counts().head(10).reset_index()
    top_sellers.columns = ["Seller ID", "Jumlah Produk Terjual"]
    fig5 = px.bar(top_sellers, x="Jumlah Produk Terjual", y="Seller ID", orientation="h",
                  color="Jumlah Produk Terjual", color_continuous_scale="Magma",
                  title="Top 10 Seller dengan Penjualan Terbanyak")
    st.plotly_chart(fig5)

elif option == "Top 10 Kota dengan Pelanggan Terbanyak":
    st.title("🏙️ Top 10 Kota dengan Jumlah Pelanggan Terbanyak")
    top_cities = customers_df["customer_city"].value_counts().head(10).reset_index()
    top_cities.columns = ["Kota", "Jumlah Pelanggan"]
    fig = px.bar(top_cities, x="Jumlah Pelanggan", y="Kota", orientation="h", color="Jumlah Pelanggan",
                 color_continuous_scale="Blues", title="Top 10 Kota dengan Jumlah Pelanggan Terbanyak")
    st.plotly_chart(fig)
     # Menampilkan insight di bawah diagram
    st.subheader("📊 Insight:")
    st.write("""
    - **São Paulo** memiliki jumlah pelanggan terbanyak, kemungkinan karena populasi besar dan daya beli tinggi.
    - Kota-kota besar lainnya seperti Rio de Janeiro dan Brasília juga mendominasi, mencerminkan tingginya transaksi e-commerce di wilayah perkotaan.
    - Kota dengan jumlah pelanggan lebih sedikit dapat menjadi peluang pasar potensial bagi ekspansi bisnis.
    """)


elif option == "Distribusi Pelanggan per Negara Bagian":
    st.title("📍 Distribusi Pelanggan Berdasarkan Negara Bagian")
    state_counts = customers_df["customer_state"].value_counts().reset_index()
    state_counts.columns = ["Negara Bagian", "Jumlah Pelanggan"]
    fig = px.bar(state_counts, x="Negara Bagian", y="Jumlah Pelanggan", color="Jumlah Pelanggan",
                 color_continuous_scale="Viridis", title="Distribusi Pelanggan Berdasarkan Negara Bagian")
    st.plotly_chart(fig)
    # Menampilkan insight di bawah diagram
    st.subheader("📊 Insight:")
    st.write("""
    - **São Paulo (SP)** memiliki jumlah pelanggan tertinggi, mencerminkan dominasi pasar e-commerce di wilayah ini.
    - **Negara bagian bagian tenggara seperti Rio de Janeiro (RJ) dan Minas Gerais (MG)** juga memiliki jumlah pelanggan tinggi, menunjukkan bahwa wilayah dengan populasi besar cenderung lebih aktif dalam belanja online.
    - **Negara bagian di bagian utara dan barat daya** memiliki jumlah pelanggan lebih rendah, kemungkinan karena akses ke layanan e-commerce dan infrastruktur yang lebih terbatas.
    - **Peluang ekspansi bisnis** dapat difokuskan ke daerah dengan penetrasi e-commerce yang lebih rendah untuk meningkatkan jangkauan pasar.
    """)

elif option == "Tren Pemesanan dari Waktu ke Waktu":
    st.title("📈 Tren Pemesanan dari Waktu ke Waktu")
    filtered_orders["year_month"] = filtered_orders["order_purchase_timestamp"].dt.strftime("%Y-%m")
    orders_trend = filtered_orders.groupby("year_month").size().reset_index()
    orders_trend.columns = ["Bulan", "Jumlah Pesanan"]
    fig = px.line(orders_trend, x="Bulan", y="Jumlah Pesanan", markers=True,
                  title="Tren Pemesanan dari Waktu ke Waktu", color_discrete_sequence=["#FF5733"])
    st.plotly_chart(fig)
    # Menampilkan insight di bawah diagram
    st.subheader("📊 Insight:")
    st.write("""
    - Puncak pemesanan terjadi pada bulan **November 2017**, dengan total **lebih dari 7544 pesanan**."
    - Jumlah pemesanan terendah terjadi pada bulan **1 Oktober 2018**, dengan hanya **4 pesanan**."
    -  Tren ini dapat membantu dalam perencanaan stok dan strategi pemasaran yang lebih efektif.
    """)

elif option == "Distribusi Metode Pembayaran":
    st.title("💳 Distribusi Metode Pembayaran")
    payment_counts = order_payments_df["payment_type"].value_counts().reset_index()
    payment_counts.columns = ["Metode Pembayaran", "Jumlah Pengguna"]
    fig = px.bar(payment_counts, x="Metode Pembayaran", y="Jumlah Pengguna", 
                 color="Jumlah Pengguna", color_continuous_scale="Viridis",
                 title="Distribusi Metode Pembayaran")
    st.plotly_chart(fig)
    # Menampilkan insight di bawah diagram
    st.subheader("📊 Insight:")
    st.write("""
    Hasil analisis metode pembayaran menunjukkan bahwa mayoritas pelanggan menggunakan kartu kredit (73.92%), diikuti oleh boleto (19.04%) dan voucher (5.56%). Pembayaran dengan kartu debit relatif jarang digunakan (1.47%).
    """)

elif option == "Top 10 Seller dengan Penjualan Terbanyak":
    st.title("🏅 Top 10 Seller dengan Penjualan Terbanyak")
    top_sellers = order_items_df["seller_id"].value_counts().head(10).reset_index()
    top_sellers.columns = ["Seller ID", "Jumlah Produk Terjual"]
    fig = px.bar(top_sellers, x="Jumlah Produk Terjual", y="Seller ID", orientation="h",
                 color="Jumlah Produk Terjual", color_continuous_scale="Magma",
                 title="Top 10 Seller dengan Penjualan Terbanyak")
    st.plotly_chart(fig)
     # Menampilkan insight di bawah diagram
    st.subheader("📊 Insight:")
    st.write("""
    Analisis menunjukkan bahwa penjual dengan ID 6560211a19b47992c3666cc44a7e94c0 adalah yang paling banyak menjual produk, dengan 2.033 penjualan, diikuti oleh 4a3ca9315b744ce9f8e9374361493884 dengan 1.987 penjualan.
    """)


# Footer
st.markdown("---")
st.markdown("📊 **E-Commerce Dashboard - Dibuat oleh Reni Kartika Suwandi** 🚀")
st.markdown("**email: renisuwandi1011@gmailcom**")
