import streamlit as st
import cv2
import numpy as np
import json
from roboflow import Roboflow
from plot import draw
import os
import shutil

rf = Roboflow(api_key="PEqyGZLD9xRGI4nxbZez")
project = rf.workspace("segmentation").project("blocksegment")
model = project.version(1).model


def predict(path):
    prediction = model.predict(path, confidence=25, overlap=50)
    with open('predictions/'+path.replace('.png','.json'), 'w') as f:
        json.dump(prediction.json(), f)



for file in os.listdir('segmentation-images'):
    
    opencv_image = cv2.imread('segmentation-images/'+file, cv2.IMREAD_COLOR)
    cv2.imwrite('image.png', opencv_image)
    predict('image.png')
    draw('image.png')

    shutil.copy('results/image.png', 'segmented-images/'+file)

