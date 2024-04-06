import streamlit as st
import cv2
import numpy as np
import json
from roboflow import Roboflow
from plot import draw
rf = Roboflow(api_key="sGk7rS8EgJKvMYC2gPZg")
project = rf.workspace("segmentation-9wdmf").project("website-segmentation-ij4gp")
model = project.version(1).model

def predict(path):
    prediction = model.predict(path, confidence=25, overlap=50)
    with open('predictions/'+path.replace('.png','.json'), 'w') as f:
        json.dump(prediction.json(), f)


st.title('WebPage Segmentation YoloNAS')

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Convert the file to an OpenCV image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    st.image(opencv_image, caption='Original Image')
    cv2.imwrite('image.png', opencv_image)
    predict('image.png')
    draw('image.png')

    


    # Display the grayscale image
    st.image('results/image.png', caption='Segmented Image')

