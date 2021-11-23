#!/usr/bin/env python3

# Image sequence stabilization
# Using the python_video_stab library

### Imports
from vidstab.VidStab import VidStab
import cv2
import glob
import shutil
import os

### Get image info
def get_image_info():
    # Read the image names to a list, get total number of images
    image_names = sorted(glob.glob("*.tif"))
    image_num = len(image_names)

    # Returns a tuple, so assign to two variables when calling function
    return image_names, image_num


### Add frames 
def add_frames(image_names, image_num):
    # Adding 30 extra frames as a sort of hacky workaround for the smoothing 
    # algorithm cutting off the last 30 frames (will delete the frames at the
    # end). 

    # Getting the name of the last frame to copy it.
    final_image_name = image_names[image_num - 1]
    
    # This will be a list of all the added fake frames, to be deleted at
    # the end
    fake_names = []
    
    # Makes i numbers to add the 30 extra frames
    for i in range(image_num, image_num + 30):
        # Make a fake frame name
        pieces = final_image_name.split("_")
        new_ending = "_t" + str(i).zfill(3) + ".tif"
        fake_name = "_".join(pieces[0:4]) + new_ending
    
        # Add to the list to be deleted later
        fake_names.append(fake_name)
        
        # Copy the last frame to the fake frame name
        shutil.copy(final_image_name, fake_name)

    return fake_names

### Open images and stabilizer
def open_images_and_stabilizer():
    # Starting up the stabilizer 
    stabilizer = VidStab()

    # Opening the image sequence
    image_seq = cv2.VideoCapture('2021-11-08_plate1_34C_A1_t%03d.tif')
    
    # Making sure the image sequence opened ok. 
    if (image_seq.isOpened() == False):
        print("Error opening image sequence")

    return stabilizer, image_seq


### Stabilize and write images
# This function stabilizes and writes out stabilized images.
def stabilize_and_write_images(stabilizer, image_seq, image_names, image_num):
    # Setting a counter to keep track of the frames
    counter = 0
    
    # Setting a counter to keep track of the actual images
    image_counter = 0
    
    while True:
        grabbed_frame, frame = image_seq.read()
    
        #if frame is not None:
        #    # Perform any pre-processing of frame before stabilization here
        #    pass
    
        # Pass frame to stabilizer even if frame is None
        # stabilized_frame will be an all black frame until iteration 30
    
        # Doing the actual stabilization
        stabilized_frame = stabilizer.stabilize_frame(input_frame = frame,
                                                      smoothing_window = 30)
    
        if counter >= 30 and counter < image_num + 30:
    
            #print("image is ", image_names[image_counter])
            current_image = image_names[image_counter]
            current_image_no_extension = current_image[:len(current_image)-4]
            stabilized_name = current_image_no_extension + "_stab.tif"
    
            #cv2.waitKey(0)
    
            cv2.imwrite(stabilized_name, stabilized_frame)
    
            image_counter += 1
    
        if stabilized_frame is None:
            # There are no more frames available to stabilize
            break
    
        counter += 1


### Clean fake frames
def clean_fake_frames(fake_names):
    for file in fake_names:
        os.remove(file)

### Remove dark or absent frames
# There's a problem with the microscope where sometimes it will capture very
# dark or missing images. This function checks for them, because they break the
# image stabilization. It returns TRUE if it's a good image and FALSE if it's
# dark or missing. It's called inside the stabilization function.
def check_image_quality(input_image):
    pass


### Here's the main
def main():
    # Getting image name list and total number of images. For now just works
    # in the current working directory.
    image_names, image_num = get_image_info()
    
    # Adding fake frames for the smoothing algorithm
    fake_names = add_frames(image_names, image_num)

    # Opening the image sequence and the stabilizer
    stabilizer, image_seq = open_images_and_stabilizer()

    # Do the stabilization and image writing
    stabilize_and_write_images(stabilizer, image_seq, image_names, image_num)

    # Clean up the fake frames
    clean_fake_frames(fake_names)


if __name__== "__main__":
  main()
