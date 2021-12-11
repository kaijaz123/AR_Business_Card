# AR_Business_Card
AR Business Card done by using OpenCV and OpenGL. This repository includes codes that for academic orientation purpose especially AR-related projects. Few techniques such as Aruco Marker, OpenGL API, and OpenCV libraries are utilised in this program. Please checkout the following contents for better understanding.

# Requirements:
1. OpenCV and OpenGL installation
2. Generate aruco marker
3. Camera Calibration

# Contents:
```main.py``` - main program script
```marker.py``` - script for detecting aruco marker
```objloader.py``` - load in 3d model and projection
```matrixTrasnform.py``` - script for handling model view matrix and projection matrix
```projeciton.py``` - opencv for 2d images projection 
```frame_to_videos.py``` - combine images to video

 # Notes:
 1. Calibrate your own camera and save the values into ```cam_parameter/cam_matrix.txt``` and distorted coefficient to ```cam_parameter/dist_coeff.txt```
 2. You may want to generate aruco marker and set the parameter in the ```marker.py``` unless you stick to the same marker that already in used.
 3. Pygame window is used to display the program and each frame in the window will be saved in the directory ```frames``` - you may run the script ```frame_to_videos.py``` after the demonstration and get a video result.
 
 
** *Notes that this is only for orientation academic demonstration and not for any business purpose. You may use Vuforia, Unity or any other kinds of techniques that will definitely boost the performance and produce a better result.**
 
