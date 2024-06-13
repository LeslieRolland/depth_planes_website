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

url_api = "https://depth-planes-from-2d-drn2cgfvba-od.a.run.app/"

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
div.stdownload_button > button {
    margin-top : 100px;
    align-items: center;
    justify-content: center;
}
div.stSpinner > div {
    text-align:center;
    align-items: center;
    justify-content: center;
}
</style>""", unsafe_allow_html=True)

# Création de placeholders
file_uploader_placeholder = st.empty()
image_display_placeholder = st.empty()
button_placeholder = st.empty()
image_comparision_placeholder = st.empty()
button_placeholder_slice = st.empty()
image_plans_placeholder = st.empty()

if 'step_1' not in ss:
    ss.step_1 = True
if 'step_2' not in ss:
    ss.step_2 = False
if 'finish' not in ss:
    ss.finish = False
if 'path_origin' not in ss:
    ss.path_origin = ''
if 'path_depth' not in ss:
    ss.path_depth = ''
if 'depth_data' not in ss:
    ss.depth_data = None

with st.container():

    if ss.step_1:

        ### Téléchargement de l'image
        img_file = file_uploader_placeholder.file_uploader(label='upload image', key='img1', label_visibility="collapsed") ### Load an image

        if img_file:
            img_origin = load_image(img_file)
            path_origin = save_temp_image(img_origin)
            ss.path_origin = path_origin
            image_display_placeholder.image(img_origin, use_column_width=True) ### Display the loaded image
            file_uploader_placeholder.empty()

            compute_button = button_placeholder.button("Calculer la carte de profondeur", key='button1')

            if compute_button: ### Make depth prediction with API
                # Nettoyer les placeholders
                button_placeholder.empty()
                image_display_placeholder.empty()

                # Afficher une barre de progression
                with st.spinner('Calcul en cours...'):
                    time.sleep(5)

                response = requests.get(url=f'{url_api}')
                print(response)

                # API call for the depth map
                img_data = img_file.getvalue() # Image  origine as bytes
                response = requests.post(url=f'{url_api}depthmap?',files={'file':img_data}) # Return bytes of depth map
                img_depth_data = img_file.getvalue() # Image  origine as bytes
                img_depth = Image.open(io.BytesIO(response.content))

                # Chargement de l'image de comparaison --> ici le call API
                path_depth = save_temp_image(img_depth)
                ss.path_depth = path_depth

                # Nettoyer les placeholders
                file_uploader_placeholder.empty()
                button_placeholder.empty()
                image_display_placeholder.empty()

                # Display original image VS depth image
                if path_origin and path_depth:
                    image_comparision_placeholder = image_comparison(img1=path_origin, img2=path_depth, label1="Original Image", label2="Depth map")
                    image_data = img_to_array(path_origin)
                    depth_data = img_to_array(path_depth)

                    ss.depth_data = np.array(img_depth)


                    depth_mask = create_mask_in_one(depth_data)
                    # print(depth_mask.shape)
                    # st.markdown(f"""{depth_mask}""")
                    img_depth_masks = create_mask_from_image(image_data, depth_mask)
                    # print(img_depth_masks.shape)
                    # st.markdown(f"""{img_depth_masks}""")

                    # path_masks = save_mask_image(img_depth_masks)
                    # for p in img_depth_masks:
                    #     st.image(p)
                    #     path_masks[f"plan{0}"] = array_to_image(p.astype(np.uint8))[1]

                    # # st.markdown("""{path_masks}""")

                    # # for path in path_masks.values():
                    # #     st.image(path)

                    # zip_path = create_zip_file(path_masks)

                    # with open(zip_path, "rb") as fp:
                    #     st.download_button(
                    #         label="Télécharger",
                    #         data=fp,
                    #         file_name="mask_images.zip",
                    #         mime="application/zip"
                    #     )


                    # print(ss.step_1,ss.step_2)
                    #if st.button("Compute plans split", key='button2'):
                    #     print('Go slice')
                    #     print(ss.step_1,ss.step_2)
                    #     ss.step_1 = False
                    #     ss.step_2 = True

                    #     # Afficher une barre de progression
                    #     with st.spinner('Wait for it...'):
                    #         time.sleep(5)

                    #     st.markdown("Test 2")

                    graph_3D = create_3D_plot(rgba_array=img_depth_masks)
                    st.pyplot(graph_3D, use_container_width=True)



with st.container():

    # Reset the app state
    if ss.step_2 and ss.finish:
        if st.button("Reset"):
            ss.step_1 = True
            ss.step_2 = False
