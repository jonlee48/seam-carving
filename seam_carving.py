import numpy as np
from tqdm import trange
from scipy.ndimage.filters import convolve
from numba import jit


def convolve2D(img, filter):
    assert (filter.shape[0] - 1) % 2 == 0, 'filter size should be odd'
    W = int((filter.shape[0] - 1) / 2)  # filter half width
    N_rows, N_cols = img.shape  # image height and width

    # 1. define "img_padded" whose np.array size is (N_rows + 2W, N_cols + 2W),
    # such that it corresopnds to the img padded by zero values
    img_padded = np.pad(img, ((W, W), (W, W)))

    # 2. define an empty "img_filtered," whose np.array size is (N_rows, N_cols)
    img_filtered = np.zeros((N_rows, N_cols))

    # 3. define "filter_flipped" using np.flip for convolution below
    filter_flipped = np.flip(filter)

    for i in range(N_rows):
        for j in range(N_cols):
            # 3. define "img_clipped" that corresponds to the clip of "img_padded" starting at (i,j).
            # Its size is equal to the filter,
            img_clipped = img_padded[i:1 + i + (2 * W), j:j + 1 + (2 * W)]

            # 4. ensure "img_clipped" is floating valued to avoid errors caused by integer * floating number
            img_clipped.astype('float64')

            # 5. perform cross-correlation between "img_clip" and "filter_flipped"
            img_filtered[i, j] = (img_clipped * filter_flipped).sum()

            # 6. return img_filtered
    return img_filtered


def convolve3D(img, filter):
    r = convolve2D(img[:,:,0], filter)
    g = convolve2D(img[:,:,1], filter)
    b = convolve2D(img[:,:,2], filter)
    return np.dstack((r,g,b))

'''
# This implementation is too slow
def calc_energy(im):
    sobel_x = np.array([
        [1, 2, 1],
        [0, 0, 0],
        [-1, -2, -1]
    ])
    sobel_y = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ])
    # im = im.astype('float32')
    im_x = convolve3D(im, np.flip(sobel_x))
    im_y = convolve3D(im, np.flip(sobel_y))

    # gradient direction does not matter
    im_energy = np.absolute(im_x, im_y)

    # combine into one color channel
    im_energy = im_energy.sum(axis=2)

    return im_energy
'''


def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_du = np.stack([filter_du] * 3, axis=2)

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])
    # This converts it from a 2D filter to a 3D filter, replicating the same
    # filter for each channel: R, G, B
    filter_dv = np.stack([filter_dv] * 3, axis=2)

    img = img.astype('float32')
    convolved = np.absolute(convolve(img, filter_du)) + np.absolute(convolve(img, filter_dv))

    # We sum the energies in the red, green, and blue channels
    energy_map = convolved.sum(axis=2)/3

    return energy_map

@jit
def find_seams(im):
    '''
    Code adapted from https://karthikkaranth.me/blog/implementing-seam-carving-with-python/
    returns:
    M (r,c) where M[i,j] stores the minimum energy required to get to that point from
    the top of the image (by only traversing neighboring pixels)
    B (r,c) where B[i,j] stores the index of the lowest weight seam from the above row
    '''

    im_energy = calc_energy(im)

    r, c = im.shape[:2]

    M = im_energy.copy()
    B = np.zeros_like(M, dtype=np.int)

    for i in range(1,r):
        for j in range(c):
            # handle case where there is no -1 index
            if j == 0:
                idx = np.argmin(M[i-1,j:j+2])
                B[i,j] = j + idx
                min_energy = M[i-1,j+idx]
            else:
                idx = np.argmin(M[i-1,j-1:j+2])
                B[i,j] = j + (idx - 1)
                min_energy = M[i-1,j+idx-1]
            M[i,j] += min_energy

    return M,B

@jit
def remove_seam(im):
    r, c = im.shape[:2]
    M,B = find_seams(im)

    # create a mask of pixels to remove
    mask = np.ones((r,c),dtype=np.bool)

    # work from the last row backward

    # initialize the minimum element
    j = np.argmin(M[-1])

    # mark pixels in mask that belong in the
    # minimum weight seam
    for i in reversed(range(r)):
        mask[i,j] = False
        j = B[i,j]

    # convert mask to 3 channel
    mask = np.stack([mask]*3,axis=2)

    # delete seam, resize image
    im_smaller = im[mask].reshape((r,c-1,3))

    return im_smaller


def resize_c(im, scale_c):
    r, c = im.shape[:2]
    new_c = int(c * scale_c)

    for i in trange(c - new_c):
        im = remove_seam(im)

    return im

def resize_r(im, scale_r):
    im = np.rot90(im, 1, (0, 1))
    im = resize_c(im, scale_r)
    im = np.rot90(im, 3, (0, 1))
    return im
