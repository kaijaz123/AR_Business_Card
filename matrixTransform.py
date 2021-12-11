import numpy as np
import cv2

def ProjectMatrix_Transform(MTX, width, height, near_plane=0.01, far_plane=100.0):
    P = np.zeros(shape=(4, 4), dtype=np.float32)

    fx, fy = MTX[0, 0], MTX[1, 1]
    cx, cy = MTX[0, 2], MTX[1, 2]


    P[0, 0] = 2 * fx / width
    P[1, 1] = 2 * fy / height
    P[2, 0] = 1 - 2 * cx / width
    P[2, 1] = 2 * cy / height - 1
    P[2, 2] = -(far_plane + near_plane) / (far_plane - near_plane)
    P[2, 3] = -1.0
    P[3, 2] = - (2 * far_plane * near_plane) / (far_plane - near_plane)

    return P.flatten()

def ModelViewMatrix_Transform(rvec, tvec):
    if rvec is None or tvec is None: return
    matrix = cv2.Rodrigues(rvec)[0]
    tvec = tvec.flatten().reshape((3, 1))

    inverse_matrix = np.array([[1.0 , 1.0, 1.0, 1.0],
                               [-1.0,-1.0,-1.0,-1.0],
                               [-1.0,-1.0,-1.0,-1.0]])

    # revert y and z axis
    transform_matrix = inverse_matrix * np.hstack((matrix, tvec))
    # construct into 4x4 model view matrix and transpose - opengl in column major order
    transform_matrix = np.vstack((transform_matrix,[0.0,0.0,0.0,1.0])).T

    return transform_matrix.flatten()
