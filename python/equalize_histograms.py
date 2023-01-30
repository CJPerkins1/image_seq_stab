import os
import cv2

def normalize_brightness(directory):
    """
    Normalize the mean brightness of all images in a specified directory

    Parameters:
    directory (str): The directory path containing the images

    Returns:
    None
    """
#     max_brightness = 0
# 
#     # Get the image with the highest brightness
#     for filename in os.listdir(directory):
#         if filename.endswith(".tif"):
#             img = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
#             brightness = cv2.mean(img)[0]
#             print(brightness)
#             if brightness > max_brightness:
#                 max_brightness = brightness
#     print("Max brightness is ", max_brightness)

    # Normalize the brightness of all images
    for filename in os.listdir(directory):
        if filename.endswith(".tif"):
            img = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
            print("before")
            print(type(img))
            print(img.shape)
            img = cv2.convertScaleAbs(img, alpha=200/cv2.mean(img)[0])

            print("after")
            print(type(img))
            print(img.shape)
            cv2.imwrite(os.path.join(directory, "normalized_images", filename.split(".")[0] + ".tif"), img)

# def equalize_hist(directory):
#     """
#     Perform histogram equalization on all images in a specified directory using OpenCV
# 
#     Parameters:
#     directory (str): The directory path containing the images
# 
#     Returns:
#     None
#     """
#     for filename in os.listdir(directory):
#         if filename.endswith(".tif"):
#             # Read the image
#             img = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
# 
#             ## Perform histogram equalization
#             #img_eq = cv2.equalizeHist(img)
# 
#             ## Perform contrast limited adaptive histogram equalization
#             #clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
#             #cl1 = clahe.apply(img)
# 
# 
# 
#             # Save the equalized image
#             cv2.imwrite(os.path.join(directory, "normalized_", filename.split(".")[0] + ".tif"), cl1)

normalize_brightness("/Users/warman/Desktop/fixing_image_stab/2022-06-02_run1_26C/well_D4")

