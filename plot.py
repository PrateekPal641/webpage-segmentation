import cv2
import json 

def filter_boxes(predictions):
    def is_inside(box1, box2):
        if (int(box2['x'])-int(box2['width'])/2) <= int(box1['x']) <= (int(box2['x'])+int(box2['width'])/2) and (int(box2['y'])-int(box2['height'])/2)<= int(box1['y']) <= (int(box2['y'])+int(box2['height'])/2) :
            print(box1)
            print(box2)
            print()
            return True

    for box1 in predictions:
        for box2 in predictions:
            if box1!=box2:
                if is_inside(box1=box2, box2=box1):
                    predictions.remove(box2)
                    break          
    return predictions


def draw(path):
    image = cv2.imread(path)
    with open('predictions/'+path.replace('.png', '.json'), 'r') as f:
        content = json.load(f)
    filtered_predictions = filter_boxes(content['predictions'])

    color = (255, 0, 0) 
    thickness = 3


    for prediction in filtered_predictions:
        start_point = ( int(int(prediction['x'])-int(prediction['width'])/2), int(int(prediction['y'])-int(prediction['height'])/2) )
        end_point = ( int(int(prediction['x'])+int(prediction['width'])/2), int(int(prediction['y'])+int(prediction['height'])/2) )
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    cv2.imwrite('results/'+path, image)
