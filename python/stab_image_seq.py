#!/usr/bin/env python3

# Image sequence stabilization
# Using the python_video_stab library

from vidstab.VidStab import VidStab
import cv2

import glob
import shutil
import os

# Read the image names to a list, get total number of images
image_names = sorted(glob.glob("*.jpg"))
image_num = len(image_names)

####### Add frames functionalize ################
# Adding 30 extra frames as a sort of hacky workaround for the smoothing 
# algorithm cutting off the last 30 frames (will delete later). 
# Getting the name of the last frame to copy it.
final_image_name = image_names[image_num - 1]

# This will be a list of all the added fake frames, to be deleted at
# the end
fake_names = []

# Makes i numbers to add the 30 extra frames
for i in range(image_num, image_num + 30):
    # Make a fake frame name
    pieces = final_image_name.split("_")
    new_ending = "_t" + str(i).zfill(3) + ".jpg"
    fake_name = "_".join(pieces[0:2]) + new_ending

    # Add to the list to be deleted later
    fake_names.append(fake_name)
    
    # Copy the last frame to the fake frame name
    shutil.copy(final_image_name, fake_name)


#################################################



# Starting up the stabilizer and opening the image sequence
stabilizer = VidStab()
imageseq = cv2.VideoCapture('A1_S001_t%03d.jpg')

# Making sure the image sequence opened ok. 
if (imageseq.isOpened() == False):
    print("Error opening image sequence")

# Setting a counter to keep track of the frames
counter = 0

# Setting a counter to keep track of the actual images
image_counter = 0

while True:
    grabbed_frame, frame = imageseq.read()

    #if frame is not None:
    #    # Perform any pre-processing of frame before stabilization here
    #    pass

    # Pass frame to stabilizer even if frame is None
    # stabilized_frame will be an all black frame until iteration 30

    # So add 30 frames on the end, then don't write the first or last 30
    # and you should be good. 

    # There's some error here where it's reading an empty image at the end,
    # check to make sure it's stopping at the right place.
    stabilized_frame = stabilizer.stabilize_frame(input_frame = frame,
                                                  smoothing_window = 30)

    if counter >= 30 and counter < image_num + 30:
        cv2.imshow('stabilized frame', stabilized_frame)
        
        #print("image is ", image_names[image_counter])
        current_image = image_names[image_counter]
        current_image_no_extension = current_image[:len(current_image)-4]
        stabilized_name = current_image_no_extension + "_stab.jpg"

        cv2.waitKey(0)

        cv2.imwrite(stabilized_name, stabilized_frame)

        image_counter += 1

    # Write out stabilized frames here? But will probably need to deal with 
    # the start and the end.

    #if counter == image_num:
        

    if stabilized_frame is None:
        # There are no more frames available to stabilize
        break

    counter += 1

    # Perform any post-processing of stabilized frame here
    pass

# Clean up the fake frames
for file in fake_names:
    os.remove(file)
