import pygame
import cv2
import numpy as np

from seam_carving import *

last_out = ''

def crop(im_path, scale_c, scale_r):
    print(im_path)
    name, ext = im_path.split('.')
    out_path = '{}_out.{}'.format(name, ext)

    im = cv2.imread(im_path)
    im = calc_energy(im)

    if scale_c:
        im = resize_c(im,scale_c)
    if scale_r:
        im = resize_r(im,scale_r)

    cv2.imwrite(out_path,im)
    last_out = out_path
    print(out_path)



# start the pygame interface
pygame.init()
clock = pygame.time.Clock()

# normal photo
crop('imgs/capital.jpg', 0.6, 0)

# panoramas
crop('imgs/japan_pano.jpg', 0.5, 0)
crop('imgs/italy_pano.jpg', 0.5, 0)
crop('imgs/rome_pano.jpg', 0.25, 0)

# caricatures/warps
crop('imgs/portrait.jpg', 0.3, 0.5)
crop('imgs/grumpy_cat.jpg', 0.5, 0.5)
crop('imgs/shrek.jpg', 0.6, 0.6)
crop('imgs/gw.jpg', 0.5, 0.5)

# load images into pygame
display_path = last_out
im = pygame.image.load(display_path )
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