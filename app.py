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
st.markdown(
    """
    [![GitHub Repo](https://img.shields.io/badge/GitHub-View_Repo-white?style=for-the-badge&logo=github)](https://github.com/mattmajestic/certifications)
    [![YouTube](https://img.shields.io/badge/Subscribe-Majestic_Coding-red?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@majesticcoding/videos)
    """,
    unsafe_allow_html=True
)

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
if "Issuer" in df.columns:
    unique_issuers = sorted(df["Issuer"].dropna().unique())
    st.sidebar.markdown("## 🎓 Certificate Issuers")
    st.sidebar.markdown('<ul style="list-style: none; padding-left: 0;">', unsafe_allow_html=True)

    for inst in unique_issuers:
        st.sidebar.markdown(f"<li style='list-style-type: none;'>✅ {inst}</li>", unsafe_allow_html=True)

    st.sidebar.markdown("</ul>", unsafe_allow_html=True)


st.sidebar.markdown(
    """
    Made with 
    [![Streamlit](https://img.shields.io/badge/Streamlit-black?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
    """,
    unsafe_allow_html=True
)

# Custom CSS to inject
custom_css = """
<style>
    /* Custom style for the active tab */
    .stTabs > .tablist > .react-tabs__tab--selected {
        background-color: #0e1117;
        color: #ffffff;
        font-family: 'Courier New', Courier, monospace;
    }
    /* Custom style for all tabs */
    .stTabs > .tablist > .react-tabs__tab {
        background-color: #e8e8e8;
        color: #4f4f4f;
        font-family: 'Courier New', Courier, monospace;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Tabs for viewing certificates and displaying a table
tab1, tab2 = st.tabs(["📄 Selected Certificate", "📋 Certificates Table"])

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
    display_df = df.drop(columns=["Filename"])
    st.dataframe(display_df, hide_index=True, width=1000, height=600)
