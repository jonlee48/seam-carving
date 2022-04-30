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
2. [Seam carving algorithm](#2---seam-carving-algorithm)
3. [Results](#3---results)
4. [Object removal](#4---object-removal)
5. [References](#5---references)

## 1 - Choose good pictures
These are some panoramas I captured on my travels.

{% include image names="imgs/rome_pano.jpg,imgs/italy_pano.jpg,imgs/japan_pano.jpg" captions="Roman Forum,Coast of Italy,Japan at night" height="200" %}

------
{% include image names="imgs/portrait.jpg,imgs/gw.jpg,imgs/grumpy_cat.jpg,imgs/shrek.jpg" captions="A picture of me,George Washington,Grumpy cat,Shrek" height="300" %}

### 3 - Results
{% include image names="imgs/japan_pano.jpg,imgs/japan_pano_out.jpg" captions="Japan at night,After seam carving" height="200" %}

------
{% include image names="imgs/portrait.jpg,imgs/portrait_out.jpg" captions="A picture of me,After seam carving" height="300" %}
{% include image names="imgs/grumpy_cat.jpg,imgs/grumpy_cat_out.jpg" captions="Grumpy cat,After seam carving" height="300" %}
