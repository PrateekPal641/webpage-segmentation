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
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    with open('predictions/'+path.replace('.png', '.json'), 'r') as f:
        content = json.load(f)
    filtered_predictions = filter_boxes(content['predictions'])

    color = (255, 0, 0) 
    thickness = 3

    boxes = []
    for i, prediction in enumerate(filtered_predictions):
        start_point = ( int(int(prediction['x'])-int(prediction['width'])/2), int(int(prediction['y'])-int(prediction['height'])/2) )
        end_point = ( int(int(prediction['x'])+int(prediction['width'])/2), int(int(prediction['y'])+int(prediction['height'])/2) )
        boxes.append((start_point, end_point))

    sorted_boxes = sorted(boxes, key=lambda x: (x[0][1], x[0][0]))
    for i, prediction in enumerate(sorted_boxes):
        start_point=prediction[0]
        end_point=prediction[1]
        image = cv2.putText(image, str(i), (start_point[0]+15, start_point[1]+40), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 3)
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
    cv2.imwrite('results/'+path, image)
