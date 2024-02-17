import cv2
import numpy as np

def downscale(image, percentage):
    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image

def findstart_end(img):
    yellow = cv2.inRange(img, (0, 255, 255), (0, 255, 255))
    blue = cv2.inRange(img, (255, 0, 0), (255, 0, 0))

    start = np.argwhere(yellow)[0]   
    end = np.argwhere(blue)[0]    
    start = (start[1], start[0])
    end = (end[1], end[0])

    return start, end    

def convert_to_white(img):
    converted_img = img.copy()
    yellow_lower = np.array([20, 100, 100], dtype=np.uint8)
    yellow_upper = np.array([60, 255, 255], dtype=np.uint8)
    blue_lower = np.array([90, 50, 50], dtype=np.uint8)
    blue_upper = np.array([120, 255, 255], dtype=np.uint8)  
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    yellow_mask = cv2.inRange(hsv_img, yellow_lower, yellow_upper)
    blue_mask = cv2.inRange(hsv_img, blue_lower, blue_upper)
    converted_img[np.where(yellow_mask == 255)] = [255, 255, 255]
    converted_img[np.where(blue_mask == 255)] = [255, 255, 255]
    return converted_img

def save_image(image, filename):
    cv2.imwrite(filename, image)

input_img = cv2.imread(r"C:\Users\peddu\OneDrive\Desktop\418_2024\Preprocessing\Screenshot_20240212_182933.png")
input_img = downscale(input_img,10)
input_img = convert_to_white(input_img)

save_image(input_img,"final.png")

