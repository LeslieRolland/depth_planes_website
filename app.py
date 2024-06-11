import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
from PIL import Image
import tempfile
import time

# Initialization
if 'key' not in st.session_state:
    st.session_state['step_1'] = False

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

# Inject custom CSS to hide the filename display
st.markdown("""
<style>
div[data-testid="stFileUploader"] .uploadedFileName {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

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

if st.session_state['step_1'] == False:
    img_file = st.file_uploader(label='upload image', key='img1', label_visibility="collapsed") ### Load an image
    st.session_state['step_1'] = True
if st.session_state['step_1'] == True:
    if img_file:
        img_origin = load_image(img_file)
        path_img1 = save_temp_image(img_origin)
        st.success('Step one : your image is successfully uploaded!')
        st.image(img_origin) ### Display the loaded image
        if st.button("Compute depth map", key='button1'): ### Make depth prediction with API
            # Afficher une barre de progression
            progress_bar = st.progress(0)
            for i in range(100):
                # Mise à jour de la barre de progression
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            st.success('Congrats : the depth map has been computed!')
            image = Image.open('/Users/leslierolland/code/soapoperator/depth_planes_website/Examples-of-depth-image.png')
            path_img2=save_temp_image(image)
            if img_file and image:
                image_comparison(img1=path_img1, img2=path_img2, label1="Original Image", label2="Depth map") ### Display original image VS depth image


params = {}

    #depth_planes_api_url = ''
    #response = requests.get(depth_planes_api_url, params=params)
    # prediction = response.json()
    # pred = prediction['url']











### Display all the planes

### HTML et CSS pour créer un effet de parallaxe avec plusieurs couches
# st.markdown("""
# <style>
# .parallax {
#   position: relative;
#   width: 100%;
#   height: 500px;
#   overflow-x: hidden;
#   overflow-y: hidden;
# }

# .parallax__layer {
#   position: absolute;
#   width: 100%;
#   height: 100%;
# }

# /* Ajustez ces valeurs pour créer l'effet désiré */
# .parallax__layer--back {
#   transform: translateZ(-2px) scale(2);
#   z-index: 1;
# }

# .parallax__layer--middle {
#   transform: translateZ(-1px) scale(1.5);
#   z-index: 2;
# }

# .parallax__layer--front {
#   transform: translateZ(0) scale(1);
#   z-index: 3;
# }
# </style>
# """, unsafe_allow_html=True)

# Add your images here dynamically injecting the file paths into the HTML
# html_content = f"""
# <div class="parallax">
#     <div class="parallax__layer parallax__layer--back">
#         <img src="https://www.belambra.fr/les-echappees/wp-inside/uploads/2018/08/vacances-ete-montagne-sante-bienfaits.png" alt="Background" style="width:100%;">
#     </div>
#     <div class="parallax__layer parallax__layer--middle">
#         <img src="https://www.allibert-trekking.com/uploads/media/images/thumbnails/AMin3_10-photo-montagne-chine-lac.jpeg" alt="Middle" style="width:100%;">
#     </div>
#     <div class="parallax__layer parallax__layer--front">
#         <img src="https://www.allibert-trekking.com/uploads/media/images/851-jma-montagne.jpeg" alt="Foreground" style="width:100%;">
#     </div>
# </div>
# """
# st.markdown(html_content, unsafe_allow_html=True)
