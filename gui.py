import pygame
import cv2
import numpy as np

from seam_carving import *


# start the pygame interface
pygame.init()
clock = pygame.time.Clock()


# resizing
im_path = 'capital.jpg'
# panos
im_path = 'japan_pano.jpg' #0.5 c
#im_path = 'italy_pano.jpg' # 0.5 c
#im_path = 'rome_pano.jpg' #0.25 c (very small), 0.5 normal

# caricatures/warps
#im_path = 'portrait.jpg' # 0.3,0.5
#im_path = 'grumpy_cat.jpg' # 0.5,0.5
#im_path = 'shrek.jpg' # 0.6,0.6
#im_path = 'gw.jpg' # 0.6,0.6; 0.5, 0.5

out_path = 'out.jpg'


im = cv2.imread(im_path)
print(im.shape)
out = calc_energy(im)
out = resize_c(im,0.5)
#out = resize_r(out,0.25)
print(out.shape)

cv2.imwrite(out_path,out)





# load images into pygame
im = pygame.image.load(out_path)
# start display with first image
screen = pygame.display.set_mode((im.get_width(), im.get_height()))  # window dimensions same as image
# Show the image
screen.blit(im, (0, 0))


quit = False
while not quit:

    # process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        # mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            pass

    # update the display
    pygame.display.flip()
    clock.tick(30)