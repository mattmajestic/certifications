import streamlit as st
import os
import base64

# Set page title and favicon
st.set_page_config(page_title="Coursera Certificates Viewer", page_icon=":mortar_board:")

# Set the directory path
dir_path = 'coursera'

# Get a list of all PDF files in the directory
pdf_files = [f for f in os.listdir(dir_path) if f.endswith('.pdf')]

# Add a title and a subtitle with emojis
st.title('Coursera Certificates Viewer :mortar_board:')
st.markdown('This app allows you to view your Coursera certificates. :point_left:')

# Create a sidebar in the Streamlit app to select a certificate
st.sidebar.markdown('## Select a Certificate :scroll:')
selected_cert = st.sidebar.selectbox('', pdf_files)

# Parse the selected certificate's name
cert_name = ' '.join(selected_cert.split('-')).title()
st.markdown(f'## Viewing Certificate: {cert_name} :scroll:')

# Display the certificate
st.markdown('### Certificate :page_facing_up:')
with open(os.path.join(dir_path, selected_cert), "rb") as file:
    base64_pdf = base64.b64encode(file.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)