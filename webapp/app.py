# Importing required libraries, obviously
import streamlit as st
from PIL import Image
import os
import utils
import zipfile
import streamlit.components.v1 as components

def page_setup():
    st.set_page_config(page_title='Pest Counter')
    st.title("Pest Counter")
    st.header(":bug: :honeybee: :ant: :beetle: :snail:")
    st.write("**We count bugs**")
    st.write("\nUpload an image of a flypaper to count the number of insects")
    st.write(open("potato.txt").read())
    utils.set_bg_image('bg.jpg')

    #hides hamgurger in upper right and "made with streamlit" footer
    hide_streamlit_style = """
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            h1, h2, p {
                text-align:center;
            }

        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

def main():
    page_setup()

    image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])

    if image_file is not None:
    	image = Image.open(image_file)
    	if st.button("Process"):
    		utils.detect_bugs(image=image)

if __name__ == "__main__":
    main()