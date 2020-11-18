# Importing required libraries, obviously
import streamlit as st
import cv2
from PIL import Image
import numpy as np
import os

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
    os.mkdir("images")
    for keypoint in keypoints:
        filename = 1
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])
        size = int(keypoint.size)
        crop = img[max(1,y-2*size): min(height-1,y+2*size), max(1,x-2*size): min(width-1,x+2*size)]
        st.image(crop, use_column_width = False)
        cv2.imwrite("images/" + str(filename) + ".jpg", crop)
    # Display found keypoints
    return imgKeyPoints


def about():
	st.write(
		'''
		hello there 

		Something

			1. :)
			2. something else
			3. bugs
			4.(\(\  
			5.( ^.^)  
			6.(,)(,)  


have a nice day
		''')


def main():
    st.title("Pest Counter App :sunglasses: ")
    st.write("**We count bugs**")

    activities = ["Home", "About"]
    choice = st.sidebar.selectbox("Pick something fun", activities)

    if choice == "Home":
    	st.write("Go to the About section from the sidebar to learn more about it.")
    	image_file = st.file_uploader("Upload image", type=['jpeg', 'png', 'jpg', 'webp'])
    	if image_file is not None:
    		image = Image.open(image_file)
    		if st.button("Process"):
    			detect_bugs(image=image)
    			#st.image(result_img, use_column_width = True)
    			#st.success("Found {} faces\n".format(len(result_faces)))

    elif choice == "About":
    	about()


if __name__ == "__main__":
    main()
