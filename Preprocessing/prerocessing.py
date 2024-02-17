import cv2
import numpy as np

def downscale(image, percentage): 
    """ Downscalong for faster computation"""
    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image

def convert_to_black_and_white(img):
    """idk why but the solve algo is only working on bw images so here we are"""
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_img, 240, 255, cv2.THRESH_BINARY)
    return cv2.cvtColor(thresh, cv2.COLOR_GRAY2BGR)

def convert_to_white(img):
    """removing the yellow and blue parts from the images"""
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
input_img = convert_to_black_and_white(input_img)

save_image(input_img,"processsed.png")

