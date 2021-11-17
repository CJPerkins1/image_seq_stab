#!/usr/bin/env python3

# Image sequence stabilization
# Using the python_video_stab library

from vidstab.VidStab import VidStab
import cv2

stabilizer = VidStab()
vidcap = cv2.VideoCapture('A1_S001_t%03d.jpg')

# Making sure the image sequecne opened ok. 
if (vidcap.isOpened() == False):
    print("Error opening image sequence")

while True:
    grabbed_frame, frame = vidcap.read()

    #print("Showing image")

    #cv2.imshow('Original frame', frame)
    #cv2.waitKey(0)

    if frame is not None:
        # Perform any pre-processing of frame before stabilization here
        pass

    # Pass frame to stabilizer even if frame is None
    # stabilized_frame will be an all black frame until iteration 30

    # So add 30 frames on the end, then don't write the first or last 30
    # and you should be good. 

    # There's some error here where it's reading an empty image at the end,
    # check to make sure it's stopping at the right place.
    stabilized_frame = stabilizer.stabilize_frame(input_frame=frame,
                                                  smoothing_window=30)

    cv2.imshow('stabilized frame', stabilized_frame)
    cv2.waitKey(0)

    # Write out stabilized frames here? But will probably need to deal with 
    # the start and the end.

    if stabilized_frame is None:
        # There are no more frames available to stabilize
        break

    # Perform any post-processing of stabilized frame here
    pass

