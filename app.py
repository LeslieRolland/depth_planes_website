import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
import streamlit.components.v1 as components
from PIL import Image
import tempfile
import time
import io

url_api = "http://127.0.0.1:8000/"

st.set_page_config(
    page_title="Depth Planes", # => Quick reference - Streamlit
    page_icon="📸",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

st.markdown("""
<h1 style='text-align: center; color: black;'>Depth Planes from 2D</h1>
<h4 style='text-align: center; color: grey;'>Upload your image</h4>
""", unsafe_allow_html=True)

### CSS pour centrer le bouton
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
</style>
""", unsafe_allow_html=True)

# CSS personnalisé pour centrer le spinner
st.markdown("""
  <style>
  div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
  }
  </style>""", unsafe_allow_html=True)

### Loading an image
def load_image(image_file):
    if image_file is not None:
        image = Image.open(image_file)
        return image
    return None

def save_temp_image(image):
    if image is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp:
            image.save(tmp.name)
            return tmp.name
    return None

# Création de placeholders
file_uploader_placeholder = st.empty()
image_display_placeholder = st.empty()
button_placeholder = st.empty()

### Téléchargement de l'image
img_file = file_uploader_placeholder.file_uploader(label='upload image', key='img1', label_visibility="collapsed") ### Load an image


if img_file:
    img_origin = load_image(img_file)
    path_img1 = save_temp_image(img_origin)
    image_display_placeholder.image(img_origin, use_column_width=True) ### Display the loaded image
    file_uploader_placeholder.empty()

    compute_button = button_placeholder.button("Compute depth map", key='button1')

    if compute_button: ### Make depth prediction with API
        # Nettoyer les placeholders
        button_placeholder.empty()
        image_display_placeholder.empty()

        # Afficher une barre de progression
        with st.spinner('Wait for it...'):
            time.sleep(5)

        # API call for the depth map
        img_data = img_file.getvalue() # To read file as bytes
        response = requests.post(url=f'{url_api}depthmap?',files={'file':img_data})
        response_img = Image.open(io.BytesIO(response.content))

        # Chargement de l'image de comparaison --> ici le call API
        image_depth = response_img
        path_img2 = save_temp_image(image_depth)

        # Nettoyer les placeholders
        file_uploader_placeholder.empty()
        button_placeholder.empty()
        image_display_placeholder.empty()

        # Display original image VS depth image
        if path_img1 and path_img2:
            image_comparison(img1=path_img1, img2=path_img2, label1="Original Image", label2="Depth map")



params = {}
