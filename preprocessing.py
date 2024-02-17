import cv2
import numpy as np

def downscale(image, percentage:float = 100):
    #for this function, it isn't recommended to keep the downscaling % param as a constant value,
    #as it messes things up for mazes with more paths
    #will need to figure out how we can set this value so it doesn't mess up things

    #if this value is wrong then the program gets stuck 
    #which reminds me, test case where there is no path?
    """ Downscaling for faster computation"""
    width = int(image.shape[1] * percentage / 100)
    height = int(image.shape[0] * percentage / 100)
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image

def convert_to_black_and_white(img):
    """Function that converts image to black and white for easier computation"""
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

def main_preprocessing(input_img_path,downscale_factor):
    input_img = cv2.imread(input_img_path)
    input_img = downscale(input_img,downscale_factor)
    input_img = convert_to_white(input_img)
    input_img = convert_to_black_and_white(input_img)
    save_image(input_img,"processed.png")

