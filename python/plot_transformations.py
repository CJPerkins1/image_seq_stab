#!/usr/bin/env python3

from vidstab import VidStab
import matplotlib.pyplot as plt

stabilizer = VidStab()
stabilizer.stabilize(input_path = 'input_video.mov', output_path = 'stable_video.avi', smoothing_window = 10)

stabilizer.plot_trajectory()
plt.show()

stabilizer.plot_transforms()
plt.show()
