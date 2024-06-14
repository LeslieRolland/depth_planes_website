import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
import streamlit.components.v1 as components
from streamlit import session_state as ss
from utils.mask import *
from utils.data import *
from PIL import Image
import tempfile
import time
import io

st.set_page_config(
    page_title="Depth Planes", # => Quick reference - Streamlit
    page_icon="📸",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed

st.markdown("""
<h1 style='text-align: center; color: black;'>Cartes de profondeur</h1>
<h4 style='text-align: center; color: grey;'>Révélez les dimensions cachées d'une image</h4>
""", unsafe_allow_html=True)

### CSS pour centrer le bouton
st.markdown("""
<style>
div.stButton > button:first-child {
    display: block;
    margin: 0 auto;
}
<style>
    div.stdownload_button > button {
        margin-top : 100px;
        align-items: center;
        justify-content: center;
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

def main():
    # Initialisation des états
    if 'path_origin' not in st.session_state:
        st.session_state['path_origin'] = None
    if 'path_depth' not in st.session_state:
        st.session_state['path_depth'] = None

    # Création de placeholders
    file_uploader_placeholder = st.empty()
    image_display_placeholder = st.empty()
    button_placeholder = st.empty()
    image_comparision_placeholder = st.empty()
    image_plans_placeholder = st.empty()

    ### Téléchargement de l'image
    img_file = file_uploader_placeholder.file_uploader(label='upload image', key='img1', label_visibility="collapsed") ### Load an image

    if img_file:
        img_origin = load_image(img_file)
        path_origin = save_temp_image(img_origin)
        st.session_state['path_origin'] = path_origin
        image_display_placeholder.image(img_origin, use_column_width=True)
        file_uploader_placeholder.empty()


        compute_button = button_placeholder.button("Calculer la carte de profondeur", key='button1')

        if compute_button:
            file_uploader_placeholder.empty()
            button_placeholder.empty()
            image_display_placeholder.empty()

            # Afficher une barre de progression
            with st.spinner('Calcul en cours...'):
                time.sleep(3)

            # Chargement de l'image de comparaison
            img_depth_local = load_image('data/img_depth.jpg')
            path_depth = save_temp_image(img_depth_local)
            st.session_state['path_depth'] = path_depth

            # Display original image VS depth image
            if st.session_state['path_origin'] and st.session_state['path_depth']:
                image_comp = image_comparison(
                    img1=st.session_state['path_origin'],
                    img2=st.session_state['path_depth'],
                    label1="Image originale",
                    label2="Carte de profondeur"
                    )

    if 'path_depth' in st.session_state and st.session_state['path_depth']:
        if button_placeholder.button("Découper les plans", key='button2'):
            file_uploader_placeholder.empty()
            button_placeholder.empty()
            image_display_placeholder.empty()
            image_display_placeholder.image('data/3D.jpg', use_column_width=True)



if __name__ == "__main__":
    main()
