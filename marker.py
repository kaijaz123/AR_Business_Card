import cv2
import cv2.aruco as aruco
import numpy as np
import matplotlib.pyplot as plt
import math

def findArcuoMarker(img, camera_matrix, dist_coeff, frame_seq):
    bbox = None
    rvec = None
    tvec = None
    markerSize = 6
    totalMarkers = 250

    # initialize marker dict
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    # detect marker
    bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters = arucoParam,
                                              cameraMatrix = camera_matrix, distCoeff = dist_coeff)

    if len(bbox) > 0:
        frame_seq += 1
        rvec, tvec, _ = aruco.estimatePoseSingleMarkers(bbox, 0.05, camera_matrix, dist_coeff)
        # draw circle on the center of marker
        marker_bbox = bbox[0][0]
        width, height = (max(marker_bbox[:,0])-min(marker_bbox[:,0]), max(marker_bbox[:,1])-min(marker_bbox[:,1]))
        cv2.circle(img, (int(min(marker_bbox[:,0])+width/2),int(min(marker_bbox[:,1])+height/2)), 10, (0,255,0), cv2.FILLED)

    return rvec, tvec, bbox, img, frame_seq
