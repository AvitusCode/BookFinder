import cv2 as cv
import Plotter


def prepare_raw_data(g):
    """
    The function transforms the image into a shades of gray.
    It is important to the easyOCR training algorithms
    :param g is a global constants:
    """

    data_size = g.train_data_count + 1
    for idx in range(1, data_size):
        img_source_pth = f"raw_train_data/td{idx}.jpg"

        image = cv.imread(img_source_pth)
        if image is None:
            raise ValueError(img_source_pth)

        image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        if g.is_debug:
            Plotter.image_plot(image_gray)

        img_out_pth = f"prepared_train_data/td{idx}.jpg"

        check = cv.imwrite(img_out_pth, image_gray)
        if not check:
            print(f"WARNING: td{idx}.jp was not saved!")
