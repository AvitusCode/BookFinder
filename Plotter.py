import matplotlib.pyplot as plt
import cv2 as cv


def image_plot(img, color='gray'):
    if color == 'gray':
        plt.imshow(img, cmap='gray', interpolation='none')
        plt.show()
    else:
        plt.imshow(cv.cvtColor(img, cv.COLOR_BGR2RGB))
        plt.show()
