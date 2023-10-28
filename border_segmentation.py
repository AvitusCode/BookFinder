import math
import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import Plotter
import Book

# Some utility functions for work flow
DEBUG: bool = True # for debugability


def canny_border(img, low_threshold, high_threshold):
    canny_edges = cv.Canny(img, low_threshold, high_threshold)

    if DEBUG:
        print('Canny edges: ')
        Plotter.image_plot(canny_edges)

    return canny_edges


def gauss_blur(img, filter_size, sigma):
    blured = cv.GaussianBlur(img, (filter_size, filter_size), sigma)

    if DEBUG:
        print("Gauss blur")
        Plotter.image_plot(blured)

    return blured


def close_image(img, x, y):
    """
    With this function we can make our borders more visible
    """
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (x, y))
    closed = cv.morphologyEx(img, cv.MORPH_CLOSE, kernel)

    if DEBUG:
        print('Close image')
        Plotter.image_plot(closed)

    return closed


def connected_components(edge_map):
    """
    Connected components are detected in the edge map, that we arrived from canny algo
    """
    levels, proc_img = cv.connectedComponents(edge_map, connectivity=8)

    if DEBUG:
        print('Find connected components, levels=', levels)
        print(proc_img.ravel())
        plt.hist(proc_img.ravel(), levels-1, [2, levels])
        plt.show()
        Plotter.image_plot(proc_img)

    return proc_img, levels


def remove_short_clusters(img, levels, threshold=200):
    hist = [0 for _ in range(levels)]

    for i in range(len(img)):
        for j in range(len(img[i])):
            hist[img[i][j]] += 1

    max_freq = []
    new_img = np.zeros(img.shape)
    np.copyto(new_img, img)

    for i in range(1, levels):
        if hist[i] > threshold:
            max_freq.append(i)

    for freq in max_freq:
        new_img[img == freq] = 255

    for i in range(len(img)):
        for j in range(len(img[i])):
            if new_img[i][j] != 255:
                new_img[i][j] = 0

    if DEBUG:
        print("Clusters {} with threshold {}".format(len(max_freq), threshold))
        print("Remove short clusters")
        Plotter.image_plot(new_img)

    return new_img


def clip_line(x1, y1, x2, y2, r):
    y1 = -y1
    y2 = -y2

    if x2 - x1 == 0:
        return x1, 0, x2, r - 1, 90

    m = (y2 - y1) / (x2 - x1)
    theta = math.degrees(math.atan(m))

    x1_new = x1 - (y1 / m)
    x2_new = x1 + (-r - y1) / m

    return int(x1_new), 0, int(x2_new), r - 1, theta


def HoughLines(img, image, min_votes):
    lines = cv.HoughLines(img.astype('uint8'), 1, np.pi / 180, min_votes)
    r, c = img.shape

    output = image.copy()

    all_theta = []
    actual_theta = []
    points = []
    temp_points = []

    for values in lines:
        rho, theta = values[0]
        all_theta.append(math.degrees(theta))

        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)

        x3, y3, x4, y4, t = clip_line(x1, y1, x2, y2, r)
        actual_theta.append(t)
        temp_points.append([(x3, y3), (x4, y4), t])

    theta_values = {}
    for theta in actual_theta:
        theta = np.abs(int(theta))
        if theta in theta_values.keys():
            theta_values[theta] += 1
        else:
            theta_values[theta] = 1

    print(theta_values)
    dominant_dir = max(theta_values, key=theta_values.get)
    print("Dominant Direction", dominant_dir)

    for p in temp_points:
        (x3, y3), (x4, y4), t = p

        if dominant_dir + 10 > np.abs(int(t)) > dominant_dir - 10:
            points.append([(x3, y3), (x4, y4), t])
            cv.line(output, (x3, y3), (x4, y4), (0, 255, 255), 2)

    if DEBUG:
        print("Lines detected :", lines.shape)
        Plotter.image_plot(output, color="color")

    return points


# Lines merging algorithm
def make_points_set(points):
    pset = []
    i = 0
    while i < len(points):
        t = []

        while i < len(points) - 1:
            if points[i + 1][0][0] - points[i][0][0] <= 20:
                t.append(i)
                i += 1
            else:
                break

        t.append(i)
        pset.append(t)
        i += 1

    return pset


def take_new_points(points_set, points):
    new_points = []

    for p in points_set:
        sum_x1 = 0
        sum_x2 = 0
        for j in p:
            sum_x1 += points[j][0][0]
            sum_x2 += points[j][1][0]

        sum_x1 /= len(p)
        sum_x2 /= len(p)

        new_points.append([(int(sum_x1), points[j][0][1]), (int(sum_x2), points[j][1][1]), points[j][2]])

    return new_points


def merge_lines(points, image):
    points.sort(key=lambda point: point[0][0])
    points = points

    pset = make_points_set(points)
    new_points = take_new_points(pset, points)

    # MERGING FROM BOTTOM
    pset = make_points_set(new_points)
    new_points2 = take_new_points(pset, new_points)

    if image.shape[1] - new_points2[-1][0][0] >= 50:
        new_points2.append([(image.shape[1] - 5, 0), (image.shape[1] - 5, image.shape[0] - 1), 90])

    output = image.copy()

    for p in new_points2:
        cv.line(output, (p[0][0], p[0][1]), (p[1][0], p[1][1]), (0, 255, 0), 2)

    if DEBUG:
        print("Merge Lines", pset)
        print(new_points2)
        Plotter.image_plot(output, color="color")

    return new_points, output


# Main working function
def get_book_border(img_path, resize: int = 1024):

    image = cv.imread(img_path)

    # books counter pipeline founder
    r = float(resize) / image.shape[1]
    dim = (resize, int(image.shape[0] * r))
    image = cv.resize(image, dim, interpolation=cv.INTER_AREA)

    print(image.shape)

    # Main pipeline (maybe incapsulate it into the class?)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    edged = canny_border(gray, 50, 150)
    proc_img, levels = connected_components(edged)
    proc_img = remove_short_clusters(proc_img, levels, threshold=200)
    points = HoughLines(proc_img, image, 130)
    points, proc_img = merge_lines(points, image)

    books = []
    for i in range(len(points) - 1):
        book_points = list()

        book_points.append(points[i][0][0]) # x0
        book_points.append(points[i][0][1]) # y0
        book_points.append(points[i + 1][1][0]) # x1
        book_points.append(points[i + 1][1][1]) # y1

        books.append(Book.BoundingBox(book_points))

    return image, books
