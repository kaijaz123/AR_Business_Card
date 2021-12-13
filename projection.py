import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import copy

def projection2D(frame, edu_frame, marker_bbox, order, prev_homo):
    if len(marker_bbox) < 1: return frame

    homography_matrix=None
    dst=None
    marker_bbox = marker_bbox[0][0]

    # load in images for projection later
    ppicture = cv2.imread("src/pp.jpeg")
    ppicture2 = cv2.imread('src/pp2.png')
    properties = cv2.imread("src/properties.png")

    # rescale the image based on the image size
    scale = 2.5
    pp2_resize = cv2.resize(ppicture2, (int(ppicture2.shape[1]//scale),int(ppicture2.shape[0]//scale)),
                            interpolation = cv2.INTER_AREA)
    edu_frame = cv2.resize(edu_frame, (int(edu_frame.shape[1]//(scale-0.5)),int(edu_frame.shape[0]//(scale-0.5))),
                           interpolation = cv2.INTER_AREA)
    properties_resize = cv2.resize(properties, (int(properties.shape[1]//scale),int(properties.shape[0]//scale)),
                                   interpolation = cv2.INTER_AREA)

    # make copy for each picture projection
    ppicture2_point = np.copy(marker_bbox)
    properties_point = np.copy(marker_bbox)
    edu_point = np.copy(marker_bbox)
    width, height = (max(marker_bbox[:,0])-min(marker_bbox[:,0]), max(marker_bbox[:,1])-min(marker_bbox[:,1]))

    # order - make a gap for 2 frames to overlay next items
    if order >= 13:
        # adjust the position
        ppicture2_point[:,0] += (width + frame.shape[1]//10)
        frame, homo = overlay(frame, pp2_resize, ppicture2_point, prev_homo[0])
        prev_homo[0] = homo

    if order >= 15:
        # adjust the position
        properties_point[:,0] += (width + frame.shape[1]//10)
        properties_point[:,1] += (height + (frame.shape[0]//9))
        frame, homo = overlay(frame, properties_resize, properties_point, prev_homo[1])
        prev_homo[1] = homo

    if order >= 17:
        # adjust the position
        edu_point[:,0] -= (width + (frame.shape[0]//9) + 20)
        edu_point[:,1] += (height + (frame.shape[0]//9))
        frame, homo = overlay(frame, edu_frame, edu_point, prev_homo[2], False)
        prev_homo[2] = homo

    return frame, prev_homo


def overlay(frame, picture, marker_bbox, prev_homo, deskew=False):
    # warp image
    img = cv2.imread("src/qr.png")
    width, height = (max(marker_bbox[:,0])-min(marker_bbox[:,0]), max(marker_bbox[:,1])-min(marker_bbox[:,1]))
    img_points = np.float32([[0,0],[img.shape[1],0],[img.shape[1],img.shape[0]],[0,img.shape[0]]])

    # accumulate the homopgrahy matrix - prevent vibration that will
    # severely affect the stability of homopgrahy matrix
    homography_matrix, _ = cv2.findHomography(img_points,marker_bbox,cv2.RANSAC,5)
    if prev_homo is not None:
        cv2.accumulateWeighted(prev_homo, homography_matrix, 0.85)
    prev_homo = homography_matrix

    warpedImg = cv2.warpPerspective(picture, homography_matrix, (frame.shape[1],frame.shape[0]),
                                    flags = cv2.INTER_NEAREST + cv2.INTER_LINEAR, borderMode = cv2.BORDER_CONSTANT)

    # deskew image
    if deskew:
        deskew_img = deskew_transform(warpedImg)
        y,x,z = np.where(deskew_img > 0)
        min_x = min(x)+5
        max_x = max(x)-5
        min_y = min(y)+5
        max_y = max(y)-5
        frame[min_y:max_y,min_x:max_x] = deskew_img[min_y:max_y,min_x:max_x]
        return frame, prev_homo

    # overlay to original frame from warped image
    x,y,z = np.where(warpedImg > 0)
    frame[x,y,z] = warpedImg[x,y,z]

    return frame, prev_homo

def deskew_transform(warpedImg):
    h,w = warpedImg.shape[:2]
    center = (w//2, h//2)

    gray = cv2.cvtColor(warpedImg, cv2.COLOR_BGR2GRAY)
    coords = np.column_stack(np.where(gray>0)).astype(np.float32)
    coords = coords[:,:2]
    temp_coords = np.copy(coords)
    coords[:,0] = temp_coords[:,1]
    coords[:,1] = temp_coords[:,0]

    _,_,angle = cv2.minAreaRect(coords)
    if angle >= 80: return warpedImg

    if angle < -45:
        angle = -(90+angle)
    elif angle < 1:
        angle = 1

    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(warpedImg, matrix, (w,h),
                             flags = cv2.INTER_CUBIC)

    return rotated
