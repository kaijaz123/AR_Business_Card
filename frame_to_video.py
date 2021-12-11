import cv2
import os

image_folder = 'frames'
video_name = 'output.avi'

images = [img for img in sorted(os.listdir(image_folder), key=lambda x:x.split(".")[0][-3:])]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape
fps = 25

video = cv2.VideoWriter(video_name, 0, fps, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()
