import streamlit as st
import os
import pandas as pd

# Set the directory path for images
dir_path = 'img'

# Set page title and favicon
st.set_page_config(page_title="Coursera Certificates Viewer", page_icon="🎓")

@st.cache_data
def load_data():
    """Load certificate data from JSON file."""
    return pd.read_json('data.json')

# Load certificate data
df = load_data()

# Ensure required columns exist
required_columns = {"Name", "Filename"}
if not required_columns.issubset(df.columns):
    st.error(f"Error: Missing required columns! Expected {required_columns}, found {set(df.columns)}")
    st.stop()

# Map Name → Filename
cert_map = dict(zip(df["Name"], df["Filename"]))

# Title and subtitle
st.title('🎓 Coursera Certificates Viewer')
st.markdown("Easily view and manage your Coursera certificates. 🏆")

# Sidebar
st.sidebar.markdown(f"## 📜 You have **{len(cert_map)}** certificates.")

# Certificate selection (by Name)
selected_cert_name = st.sidebar.selectbox("Select a Certificate", list(cert_map.keys()))

# Get corresponding filename
selected_cert_filename = cert_map[selected_cert_name]

# Apply custom global CSS (removes bullet points from lists)
st.markdown(
    """
    <style>
    ul { 
        list-style-type: none;  /* Removes bullet points */
        padding-left: 0;  /* Removes extra padding */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Get unique institutions if available
if "Institute" in df.columns:
    unique_institutions = sorted(df["Institute"].dropna().unique())
    st.sidebar.markdown("## 🏫 Institutions")
    st.sidebar.markdown("<ul>", unsafe_allow_html=True)
    for inst in unique_institutions:
        st.sidebar.markdown(f"<li>✅ {inst}</li>", unsafe_allow_html=True)
    st.sidebar.markdown("</ul>", unsafe_allow_html=True)

# Tabs for viewing certificates and displaying a table
tab1, tab2 = st.tabs(["📄 View Certificate", "📋 Certificates Table"])

with tab1:
    st.markdown(f"### 📜 Viewing Certificate: {selected_cert_name}")
    
    # Display the selected certificate image (if exists)
    image_path = os.path.join(dir_path, selected_cert_filename)
    if os.path.exists(image_path):
        st.image(image_path, caption=selected_cert_name, use_container_width=True)
    else:
        st.warning("⚠️ Certificate image not found!")

with tab2:
    st.markdown("### 📜 All Certificates")
    display_df = df.drop(columns=["Filename"])  # Hide Filename column
    st.dataframe(display_df.reset_index(drop=True), width=1000, height=600)
