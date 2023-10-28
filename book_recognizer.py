import Book
import math
import Plotter as plt
import Rotating as rot
import easyocr

# easy ocr configuration
reader = easyocr.Reader(['ru', 'en'], gpu=False)
DEBUG: bool = True


def recognize_text(image):
    result = reader.readtext(image, detail=1, paragraph=False)
    output = []
    for (bbox, text, prob) in result:
        output.append(text)
    return output


def book_recognizer(image, borders):
    books = []

    for border in borders:
        # TODO: The algorithm should rotate the image at angles 0, 90, 180, 270 and try to recognize the text
        try:
            cropped_image = image[border.y0:border.y1, border.x0:border.x1]
            image_height, image_width = cropped_image.shape[0:2]
            image_rotated = rot.rotate_image(cropped_image, 90)
            image_rotated_cropped = rot.crop_around_center(
                image_rotated,
                *rot.largest_rotated_rect(
                    image_width,
                    image_height,
                    math.radians(90)
                )
            )

            if DEBUG:
                plt.image_plot(image_rotated_cropped, color='color')

            image_text = recognize_text(image_rotated_cropped)
            print(image_text)
            # TODO: match text with the books data base and append result to the books container
            #  (match success else nothing)

        except ValueError:
            print("Some error has occured")
            break
        except Exception as err:
            print(f"Unexpected {err=}, {type(err)=}")
            break

    return books