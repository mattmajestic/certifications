import streamlit as st
import os
import pandas as pd

# Set the directory path
dir_path = 'img'
# Set page title and favicon
st.set_page_config(page_title="Coursera Certificates Viewer", page_icon=":mortar_board:")

# Get a list of all PNG files in the directory
png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]

@st.cache_data
def load_data():
    return pd.read_csv('data.csv')

# Load your data
df = load_data()

# Add a title and a subtitle with emojis
st.title('Coursera Certificates Viewer :mortar_board:')
st.markdown('This app allows you to view your Coursera certificates. :point_left:')

# Display the number of certificates
st.sidebar.markdown(f'## You have **{len(png_files)}** certificates. :trophy:')

# Create a sidebar in the Streamlit app to select a certificate
st.sidebar.markdown('## Select a Certificate :scroll:')
selected_cert = st.sidebar.selectbox('', png_files)

# Extract the institution names from the filenames
institutions = [filename.split('-')[0] for filename in png_files]

# Get the unique institutions
unique_institutions = set(institutions)

# Display the unique institutions in the sidebar
st.sidebar.markdown(f'<p style="color:green;font-size:20px;">From Institutions: {", ".join(unique_institutions).title()}</p>', unsafe_allow_html=True)

# Tabs for viewing certificates and displaying a table of certificates
tab1, tab2 = st.tabs(["View Certificate", "Certificates Table"])

with tab1:
    # Parse the selected certificate's name
    cert_name = ' '.join(selected_cert.split('-')).title()
    st.markdown(f'## Viewing Certificate: {cert_name} :scroll:')
    
    # Display the selected image
    st.image(os.path.join(dir_path, selected_cert))

with tab2:
    st.markdown('## All Certificates :page_with_curl:')
    st.dataframe(df)

