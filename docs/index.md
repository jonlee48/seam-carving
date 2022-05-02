---
title: "CSCI 3907: Computational Photography "
layout: post
mathjax: true
---
------
# Final Project: Seam Carving

## Team Members
- Jonathan Lee

## Overview
Seam carving is an image operation that supports content-aware image resizing. 
The algorithm automatically removes seams - connected paths of low energy pixels in an image.
The objective is to remove enough vertical/horizontal seams to reduce the dimension of the image to the targeted size.
This technique preserves the most important parts of the image by giving it a higher weight using an energy function. 

One practical application of seam carving is adapting images to fit better on mobile devices. 
For example, the aspect ratio of panoramas makes it difficult to view in portrait-mode on a mobile device.
Thus, reshaping panoramas so all the important parts fit on a smartphone is a useful thing.

Seam carving can also be used to make automatic caricatures. 
Since seam carving preserves the important parts of images and reduces everything else, the final image will have more emphasize on prominent features. 
This results in some funny caricatures from portraits.

I tested seam carving on my own photographs and making caricatures from portraits.
The code is available [here](https://github.com/jonlee48/seam-carving).

### Sections
1. [Choose good pictures](#1---choose-good-pictures)
   1. [Panoramas](#11---panoramas)
   2. [Portraits](#12---portraits)
2. [Seam carving algorithm](#2---seam-carving-algorithm)
3. [Results](#3---results)
    1. [Panoramas](#31---panoramas)
    2. [Portraits](#32---portraits)
5. [Object removal](#4---object-removal)
6. [References](#5---references)

## 1 - Choose good pictures
### 1.1 - Panoramas
These are some panoramas I captured on my travels. These would be good tests for reducing the width of the image, while trying to maintain the landmarks in the scene.

{% include image names="imgs/rome_pano.jpg,imgs/italy_pano.jpg,imgs/japan_pano.jpg" captions="Roman Forum,Coast of Italy,Japan at night" height="200" %}

### 1.2 - Portraits
These are some portraits that would be fun to experiment with making caricatures out of.

{% include image names="imgs/portrait.jpg,imgs/gw.jpg,imgs/grumpy_cat.jpg,imgs/shrek.jpg" captions="A picture of me,George Washington,Grumpy cat,Shrek" height="300" %}

## 2 - Seam carving algorithm
The algorithm follows 4 steps:
1. Calculate the energy of each pixel
2. Make a list of seams 
3. Remove the lowest energy seam
4. Repeat steps 1-3

### 2.1 Calculate the energy of each pixel
The energy function can be defined by various algorithms: gradient magnitude, saliency measures, eye-gaze movement. 
I used the gradient magnitude, since it was simple to implement and produced effective results.

$$
e(I) = |\frac{\partial}{\partial x}I|+|\frac{\partial}{\partial y}I|
$$

The gradient of the image is calculated by convolving sobel filters with the image.

{% include image names="imgs/japan_pano_energy.jpg" captions="Energy map" height="200" %}

### 2.2 Make a list of seams 
Dynamic programming is used to compute a list of seams. A 2D array stores the minimum energy value at that point
in the image, considering all possible seams to that point from the top of the image.
The minimum energy seam will therefore be the minimum value in the last row of the array. To reconstruct the seam, 
another 2D array stores the index of the minimum seam upto that location in the image.


{% include image names="imgs/dynamic_programming_1.png,imgs/dynamic_programming_2.png" 
caption="For each pixel starting from the 2nd row, the energy is its own energy plus the minimal of the three energies above. Repeat until the bottom is reached." height="200" %}
### 2.3 Remove the lowest energy seam
To remove the lowest energy seam, backtrack from the last row in the lookup array, marking the pixels
that belong to the lowest energy seam.

{% include image names="imgs/backtracking.png" captions="From the lowest energy at the end backtrack up the rows to recover the seam with minimal energy" height="200" %}
### 2.4 Repeat
Continue reducing the width until the desired width is reached. The height of the image can also be reduced by repeating
the algorithm on the image rotated 90 degrees, and the result is rotated -90 degrees to the starting orientation.


## 3 - Results
### 3.1 - Panoramas
{% include image names="imgs/rome_pano.jpg,imgs/rome_pano_out.jpg" captions="Before,After seam carving" height="200" %}
This result looks pretty cool. It maintains the pillars and building features, while reducing space between each structure. 
It looks like a very dense version of Rome.

{% include image names="imgs/italy_pano.jpg,imgs/italy_pano_out.jpg" captions="Before,After seam carving" height="200" %}
This result also came out pretty nicely. The people on the far right, the building on the left, and the mountains look unchanged.
Most of the seams came from the ocean area. Some artifacts of the removal can still be seen, with a notable shift in color in the sky
next to the people on the balcony.

{% include image names="imgs/japan_pano.jpg,imgs/japan_pano_out.jpg" captions="Before,After seam carving" height="200" %}
This result was also very successful. The lanterns, temple, and people still look unchanged, while the space between them was removed.


### 3.2 - Portraits
{% include image names="imgs/portrait.jpg,imgs/portrait_out.jpg" captions="Before,After seam carving" height="300" %}
This caricature did not come out as smooth as I would have liked. Since I apply seam carving to the width and then the height afterward,
I don't the most optimal choices of removal that gets to the target size. 

{% include image names="imgs/gw.jpg,imgs/gw_out.jpg" captions="Before,After seam carving" height="300" %}
This one is pretty good. George is a stud.

{% include image names="imgs/grumpy_cat.jpg,imgs/grumpy_cat_out.jpg" captions="Before,After seam carving" height="300" %}
I like this one as well. It doesn't show any artifacts of the seam carving, and it really highlights Grumpy Cat's grumpiness. Good meme potential here.

{% include image names="imgs/shrek.jpg,imgs/shrek_out.jpg" captions="Before,After seam carving" height="300" %}
Shrek has some issues with the right side of his face. It seems like the algorithm carved away all the face that was in shadow, since that has a relatively flat gradient.


## 4 - Object removal
Specific regions in an image can be manually selected to be removed by the seam carving operation. The [original paper](https://faculty.runi.ac.il/arik/scweb/imret/imret.pdf)
allowed the user to mark pixels, where consecutive seams would remove the marked pixels until there none left. This resulted in some pretty convincing
object removals that would be difficult to achieve with in-painting or texture synthesis. I would like to implement a version of this once I finish my finals!

## 5 - References
- [Seam Carving for Content-Aware Image Resizing](https://faculty.runi.ac.il/arik/scweb/imret/imret.pdf) - the original paper introducing seam carving.
- [Implementing seam carving with python](https://karthikkaranth.me/blog/implementing-seam-carving-with-python/) - the dynamic programming approach to seam carving in Python
- [Seam carving](https://en.wikipedia.org/wiki/Seam_carving) - diagram of the dynamic programming process