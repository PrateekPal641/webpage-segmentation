import streamlit as st
import cv2
import numpy as np
import json
from roboflow import Roboflow
from plot import draw
from vision import fill_context_with_vision

rf = Roboflow(api_key="PEqyGZLD9xRGI4nxbZez")
project = rf.workspace("segmentation").project("blocksegment")
model = project.version(1).model


def predict(path):
    prediction = model.predict(path, confidence=20, overlap=20)
    with open('predictions/'+path.replace('.png','.json'), 'w') as f:
        json.dump(prediction.json(), f)



st.title('WebPage Segmentation YoloNAS')

# Create a file uploader widget
uploaded_file = st.file_uploader("Choose an image...", type=['jpg', 'jpeg', 'png'])

if uploaded_file is not None:
    # Convert the file to an OpenCV image.
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    opencv_image = cv2.imdecode(file_bytes, 1)
    cv2.imwrite('image.png', opencv_image)
    st.image('image.png', caption='Original Image')
    predict('image.png')
    draw('image.png')
    st.image('results/image.png', caption='Segmented Image')
    mapping = json.loads(fill_context_with_vision('results/image.png'))
    st.json(mapping)



