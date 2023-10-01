import math
import numpy as np
import cv2 as cv
import imutils
import matplotlib.pyplot as plt

# Some utility functions for work flow
DEBUG: bool = True  # for debugability


def image_plot(img, color='gray'):
    if color == 'gray':
        plt.imshow(img, cmap='gray', interpolation='none')
        plt.show()
    else:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.show()


def canny_border(img, low_threshold, high_threshold):
    canny_edges = cv.Canny(img, low_threshold, high_threshold)

    if DEBUG:
        print('Canny edges: ')
        image_plot(canny_edges)

    return canny_edges


def gauss_blur(img, filter_size, sigma):
    blured = cv.GaussianBlur(img, (filter_size, filter_size), sigma)

    if DEBUG:
        print("Gauss blur")
        image_plot(blured)

    return blured


def close_image(img, x, y):
    """
    With this function we can make our borders more visible
    """
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (x, y))
    closed = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

    if DEBUG:
        print('Close image')
        image_plot(closed)

    return closed


def find_contours(img, source, ratio):
    cnts = cv.findContours(img.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv.contourArea, reverse=True)

    for c in cnts:
        peri = cv.arcLength(c, True)
        approx = cv.approxPolyDP(c, 0.02 * peri, True)

        if len(approx) == 4:
            approx = approx.astype("float")
            approx *= ratio
            approx = approx.astype("int")
            cv.drawContours(source, [approx], -1, (0, 255, 0), 4)

    if DEBUG:
        print('contours')
        image_plot(source, color='color')


def connected_components(img):
    """
    Connected components are detected in the edge map, that we arrived from canny algo
    """
    levels, proc_img = cv.connectedComponents(img, connectivity=8)

    if DEBUG:
        print('Find connected components, levels=', levels)
        print(proc_img.ravel())
        plt.hist(proc_img.ravel(), levels-1, [2, levels])
        plt.show()
        image_plot(proc_img)

    return proc_img, levels


# Main working function
def get_book_border(img_path, resize: int = 300):

    image = cv.imread(img_path)

    # make some preparation
    resized = imutils.resize(image, width=resize)
    ratio = image.shape[0] / float(resized.shape[0])
    gray = cv.cvtColor(resized, cv.COLOR_BGR2GRAY)
    blurred = gauss_blur(gray, 5, 0)
    edged = canny_border(blurred, 60, 255)

    image = find_contours(edged, image, ratio)
