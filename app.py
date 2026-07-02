import streamlit as st
import pandas as pd
import joblib

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="AI Laptop Price Prediction",
    page_icon="💻",
    layout="wide"
)

# ==========================================
# CSS
# ==========================================
st.markdown("""
<style>
.stApp{
    background:linear-gradient(135deg,#f8fafc,#dbeafe);
}

h1{
    text-align:center;
    font-size:42px !important;
    font-weight:800 !important;
    color:#1e3a8a;
}

section[data-testid="stSidebar"]{
    background:#f8fafc;
}

section[data-testid="stSidebar"] *{
    color:black !important;
}

.stButton>button{
    width:100%;
    height:55px;
    border:none;
    border-radius:12px;
    background:linear-gradient(135deg,#2563eb,#16a34a);
    color:white !important;
    font-size:18px;
    font-weight:bold;
}

.stDownloadButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
}

div[data-testid="metric-container"]{
    background:white;
    padding:15px;
    border-radius:15px;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# LOAD MODEL
# ==========================================
try:
    model = joblib.load("model/laptop_price_model.pkl")
    columns = joblib.load("model/model_columns.pkl")
except Exception as e:
    st.error(e)
    st.stop()

# ==========================================
# TITLE
# ==========================================
st.title("💻 AI Laptop Price Prediction System")

st.markdown("""
<div style='background:white;
padding:20px;
border-radius:15px;
text-align:center;'>

<h2>🤖 AI Powered Laptop Price Prediction</h2>
<p>Predict laptop prices using Machine Learning</p>

</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.header("💻 Laptop Specifications")

brand = st.sidebar.selectbox(
    "Brand",
    ["HP","Dell","Lenovo","Apple","Acer","Asus","MSI"]
)

ram = st.sidebar.selectbox(
    "RAM (GB)",
    [4,8,16,32]
)

ram_type = st.sidebar.selectbox(
    "RAM Type",
    ["DDR4","DDR5","LPDDR4","LPDDR5"]
)

rom = st.sidebar.selectbox(
    "Storage (GB)",
    [128,256,512,1024]
)

os_name = st.sidebar.selectbox(
    "Operating System",
    ["Windows 11 OS","Windows 10 OS","Mac OS"]
)

cpu = st.sidebar.selectbox(
    "CPU Brand",
    ["Intel","Apple","Other"]
)

gpu = st.sidebar.selectbox(
    "GPU Brand",
    ["Intel","NVIDIA","Apple","Other"]
)

warranty = st.sidebar.slider(
    "Warranty",
    0,5,1
)

display_size = st.sidebar.slider(
    "Display Size",
    11.0,18.0,15.6
)

resolution = st.sidebar.number_input(
    "Resolution",
    value=1920
)

spec_rating = st.sidebar.slider(
    "Specification Rating",
    50.0,
    90.0,
    70.0
)

# ==========================================
# BRAND IMAGES
# ==========================================
images = {
    "HP":"https://cdn.mos.cms.futurecdn.net/pyL3b8cis5dcmUvgbe9ygV.jpg",
    "Dell":"https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
    "Lenovo":"https://images.unsplash.com/photo-1517336714739-489689fd1ca8",
    "Apple":"https://images.unsplash.com/photo-1517336714739-489689fd1ca8",
    "Acer":"https://images.unsplash.com/photo-1496181133206-80ce9b88a853",
    "Asus":"https://images.unsplash.com/photo-1517336714739-489689fd1ca8",
    "MSI":"https://images.unsplash.com/photo-1496181133206-80ce9b88a853"
}

# ==========================================
# PREDICT
# ==========================================
if st.button("🔍 Predict Price"):

    try:

        input_df = pd.DataFrame(
            0,
            index=[0],
            columns=columns
        )

        # Numeric
        input_df["spec_rating"] = spec_rating
        input_df["Ram"] = ram
        input_df["ROM"] = rom
        input_df["display_size"] = display_size
        input_df["warranty"] = warranty
        input_df["Resolution"] = resolution

        def set_col(prefix, value):
            col = f"{prefix}_{value}"
            if col in columns:
                input_df[col] = 1

        set_col("brand", brand)
        set_col("Ram_type", ram_type)
        set_col("OS", os_name)
        set_col("CPU_Brand", cpu)
        set_col("GPU_Brand", gpu)

        prediction = model.predict(input_df)[0]

        st.subheader("📊 Prediction Result")

        c1,c2,c3 = st.columns(3)

        with c1:
            st.metric(
                "Estimated Price",
                f"₹{int(prediction):,}"
            )

        if prediction < 40000:
            category = "Budget"
        elif prediction < 80000:
            category = "Mid-Range"
        else:
            category = "Premium"

        with c2:
            st.metric("Category", category)

        with c3:
            st.metric("Brand", brand)

        st.progress(
            min(
                int(prediction/200000*100),
                100
            )
        )

        if brand in images:
            st.image(
                images[brand],
                width=300
            )

        st.subheader("💻 Configuration")

        col1,col2 = st.columns(2)

        with col1:
            st.write(f"Brand: {brand}")
            st.write(f"RAM: {ram} GB {ram_type}")
            st.write(f"Storage: {rom} GB")

        with col2:
            st.write(f"CPU: {cpu}")
            st.write(f"GPU: {gpu}")
            st.write(f"OS: {os_name}")

        st.subheader("⭐ Recommended Models")

        recommendations = {
            "HP":["HP Pavilion","HP Victus","HP Envy"],
            "Dell":["Dell Inspiron","Dell G15","Dell XPS"],
            "Lenovo":["IdeaPad","Legion","ThinkPad"],
            "Apple":["MacBook Air","MacBook Pro"],
            "Acer":["Aspire","Nitro"],
            "Asus":["VivoBook","ROG"],
            "MSI":["Katana","Stealth"]
        }

        if brand in recommendations:
            for item in recommendations[brand]:
                st.success(item)

        report = f"""
Laptop Price Prediction Report

Brand: {brand}
RAM: {ram}
Storage: {rom}
OS: {os_name}
CPU: {cpu}
GPU: {gpu}

Predicted Price:
₹{int(prediction):,}

Category:
{category}
"""

        st.download_button(
            "📄 Download Report",
            report,
            file_name="Laptop_Report.txt"
        )

    except Exception as e:
        st.error(e)