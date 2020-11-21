import cv2
import streamlit as st
import numpy as np
import base64
import zipfile
import os
import streamlit.components.v1 as components

def detect_bugs(image):
    #Gray scale and blur the image
    img = np.array(image.convert('RGB'))
    imgGray = np.array(image.convert('L'))
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    height, width, channels = img.shape

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area.
    params.filterByArea = True
    params.minArea = 300
    #params.maxArea = 3000

    # Filter by Convexity
    params.filterByConvexity = True
    params.minConvexity = 0.01

    # Filter by Inertia
    params.filterByInertia = True
    params.minInertiaRatio = 0.01

    # Create a detector with the parameters
    detector = cv2.SimpleBlobDetector_create(params)

    #detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(imgBlur)
    imgKeyPoints = cv2.drawKeypoints(img, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Crop out keypoints
    if not os.path.exists('immages'):
        os.mkdir("immages")
    filename = 0
    for keypoint in keypoints:
        filename += 1
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        size = int(keypoint.size)
        crop = img[max(1,y-2*size): min(height-1,y+2*size), max(1,x-2*size): min(width-1,x+2*size)]
        st.image(crop, use_column_width = False)
        cv2.imwrite("immages/" + str(filename) + ".jpg", crop)

    zipdir("immages")       
    return imgKeyPoints

#stuff to set background image
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_bg_image(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return


def zipdir(path):
    # ziph is zipfile handle
    zipf = zipfile.ZipFile('tomato.zip','w')

    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))

    zipf.close()

    with open('tomato.zip', "rb") as f:
        bytes = f.read()
        b64 = base64.b64encode(bytes).decode()
        href = f'<a href="data:file/zip;base64,{b64}" download=\'croppedbugs.zip\'>\
            Click to download\
            </a>'
    st.sidebar.markdown(href, unsafe_allow_html=True)
