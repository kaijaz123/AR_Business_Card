from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import cv2
import math
from PIL import Image
import pygame
import pygame.camera

from matrixTransform import ProjectMatrix_Transform, ModelViewMatrix_Transform
from projection import projection2D
from objloader import OBJ
from marker import findArcuoMarker

class ImageLoader:
    def __init__(self, x, y):
        # initialize image settings
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.img_data = 0

    def load(self, image):
        # load in the image settings
        im = image
        tx_image = cv2.flip(im, 0)
        tx_image = Image.fromarray(tx_image)
        self.width = tx_image.size[0]
        self.height = tx_image.size[1]
        self.img_data = tx_image.tobytes('raw', 'BGRX', 0, -1)

        # load scene background as texture to opengl
        self.Texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.Texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width, self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, self.img_data)

    def draw(self):
        # draw the texture
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslate(self.x, self.y, 0)

        glEnable(GL_TEXTURE_2D)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0)
        glVertex2f(0, 0)
        glTexCoord2f(1, 0)
        glVertex2f(self.width, 0)
        glTexCoord2f(1, 1)
        glVertex2f(self.width, self.height)
        glTexCoord2f(0, 1)
        glVertex2f(0, self.height)
        glEnd()
        glDisable(GL_TEXTURE_2D)

if __name__ == '__main__':
    # card_cap = cv2.VideoCapture(0)
    card_cap = cv2.VideoCapture("src/business_card.mov")
    edu_cap = cv2.VideoCapture("src/education.mp4")

    # load camera parameter
    calibration_matrix = np.loadtxt("cam_parameter/cam_matrix.txt", delimiter = ',')
    dist_coeff = np.loadtxt("cam_parameter/dist_coefficient.txt", delimiter = ',')

    # init pygame
    pygame.init()
    width, height = int(card_cap.get(3)), int(card_cap.get(4))
    edu_video_length = int(edu_cap.get(cv2.CAP_PROP_FRAME_COUNT))
    screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

    # load 3d model
    box = OBJ('3d_models/robot/Robot.obj')

    # load background scene
    im_loader = ImageLoader(0, 0)
    glClearColor(0.7, 0, 0, 1)

    prev_homo = [None,None,None]
    angle = 0
    frame_seq = 0
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               run = False

        # set background for opengl
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluOrtho2D(0, width, height, 0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        success, frame = card_cap.read()
        if not success:
            raise ValueError("Video ends or can't be processed!")

        rvec, tvec, marker_bbox, frame, frame_seq = findArcuoMarker(frame, calibration_matrix, dist_coeff, frame_seq)

        # if aruco marker not detected
        if marker_bbox is None or frame_seq < 11:
            im_loader.load(frame)
            glColor3f(1, 1, 1)
            im_loader.draw()
            pygame.display.flip()
            continue

        # if aruco marker detected
        view_matrix = ModelViewMatrix_Transform(rvec, tvec)
        project_matrix = ProjectMatrix_Transform(calibration_matrix, width, height, 0.01, 100.0)
        if view_matrix is not None:
            if frame_seq < edu_video_length:
                sucess, edu_frame = edu_cap.read()
            frame, prev_homo = projection2D(frame, edu_frame, marker_bbox, frame_seq, prev_homo)
        im_loader.load(frame)

        glColor3f(1, 1, 1)
        im_loader.draw()

        # load projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glMultMatrixf(project_matrix)

        # load model view matrix
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        if view_matrix is not None:
            glLoadMatrixd(view_matrix)

            # adjust the projected position, rotation, and scaling
            glScaled(0.2,0.2,0.2)
            glTranslatef(0.0,-0.1,0.0)
            glRotatef(angle,0,1,0)

            # render 3d models
            glEnable(GL_DEPTH_TEST)
            box.render(view_matrix)
            box.free()

        # save pygame window frame
        if not os.path.exists("frames"):
            os.mkdir("frames")
        size = screen.get_size()
        buffer = glReadPixels(0, 0, *size, GL_RGBA, GL_UNSIGNED_BYTE)
        pygame.display.flip()

        screen_surf = pygame.image.fromstring(buffer,size,"RGBA")
        screen_surf = pygame.transform.flip(screen_surf,False,True)
        pygame.image.save(screen_surf, "frames/screenshot{}.jpeg".format(str(frame_seq).zfill(3)))

        angle += 10

    pygame.quit()
    quit()
