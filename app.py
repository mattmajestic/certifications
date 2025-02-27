import streamlit as st
import os
import pandas as pd

# Set the directory path for images
dir_path = 'img'

# Set page title and favicon
st.set_page_config(page_title="Coursera Certificates Viewer", page_icon="🎓")

@st.cache_data
def load_data():
    df = pd.read_csv('data.csv')
    df.columns = df.columns.str.strip()  # Ensure no extra spaces in column names
    return df

# Load certificate data
df = load_data()

# Ensure required columns exist
if "Name" not in df.columns:
    st.error("Error: The CSV file is missing the 'Name' column.")
    st.stop()

# Ensure no extra spaces in column names
df.columns = df.columns.str.strip()

# Use filenames as selection options
cert_map = df[["Filename", "Name"]]

# Title and subtitle
st.title('🎓 Coursera Certificates Viewer')
st.markdown("Easily view and manage your Coursera certificates. 🏆")

# Sidebar
st.sidebar.markdown(f"## 📜 You have **{len(cert_map)}** certificates.")

# Certificate selection (by Name)
selected_cert_name = st.sidebar.selectbox("Select a Certificate", cert_map["Name"].tolist())

# Get corresponding filename
selected_cert_filename = cert_map.loc[cert_map["Name"] == selected_cert_name, "Filename"].values[0]

# Apply custom global CSS
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
    st.sidebar.markdown("<ul style='list-style-type: none; padding-left: 10px;'>", unsafe_allow_html=True)
    for inst in unique_institutions:
        st.sidebar.markdown(f"<li>✅ {inst}</li>", unsafe_allow_html=True)
    st.sidebar.markdown("</ul>", unsafe_allow_html=True)

# Tabs for viewing certificates and displaying a table
tab1, tab2 = st.tabs(["📄 View Certificate", "📋 Certificates Table"])

with tab1:
    st.markdown(f"### 📜 Viewing Certificate: {selected_cert_filename}")
    
    # Display the selected certificate image (if exists)
    image_path = os.path.join(dir_path, selected_cert_filename)
    if os.path.exists(image_path):
        st.image(image_path, caption=selected_cert_filename, use_container_width=True)
    else:
        st.warning("Certificate image not found.")

with tab2:
    st.markdown("### 📜 All Certificates")
    display_df = df.drop(columns=["Filename"])
    st.dataframe(display_df.reset_index(drop=True), width=1000, height=600)

