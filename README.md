# AR_Business_Card
AR Business Card done by using OpenCV and OpenGL. This repository includes codes that for academic orientation purpose especially AR-related projects. Few techniques such as Aruco Marker, OpenGL API, and OpenCV libraries are utilised in this program. Please checkout the following contents for better understanding.

# Requirements:
1. OpenCV and OpenGL installation
2. Pygame
3. Generate aruco marker
4. Camera Calibration

# Contents:
```main.py``` - main program script

```marker.py``` - script for detecting aruco marker

```objloader.py``` - load in 3d model and projection

```matrixTrasnform.py``` - script for handling model view matrix and projection matrix

```projeciton.py``` - opencv for 2d images projection 

```frame_to_videos.py``` - combine images to video

 # Notes:
 1. Calibrate your own camera and save the values into ```cam_parameter/cam_matrix.txt``` and distorted coefficients to ```cam_parameter/dist_coefficient.txt```
 2. You may want to generate aruco marker and set the parameter in the ```marker.py``` unless you stick to the same marker that already in used.
 3. Pygame window is used to display the program and each frame in the window will be saved in the directory ```frames``` - you may run the script ```frame_to_videos.py``` after the demonstration and get a video result.
 4. Feel free to replace all the sources in the ```src``` folder. The folder includes all the iamges and videos that will be projected onto the scene. ```projection.py``` handles the 2D projection (using homography matrix) while the ```objloader.py``` handles the 3D model projection. 3D models are located in the folder ```3d_models```.

Result example (video):




https://user-images.githubusercontent.com/49195906/145685551-c793966f-bbaa-457e-b35d-8b16a318b47e.mp4





# IMPORTANT NOTE!!
This is only for academic orientation purpose and not for any business purpose. Since this a demonstration of using OpenCV and OpenGL, you may notice that small changes of scene or vibration will affect the performance. You may consider to use Vuforia, Unity or any other kinds of techniques will definitely boost the performance and produce a better result.
 
