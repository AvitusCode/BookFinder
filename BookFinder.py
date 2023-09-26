import Book


def main():
    print("Starting the service")
    points = [0, 0, 2, 2]

    box = Book.BoundingBox(points)
    xc, yc = box.center()

    print("BoundingBox center is ({}, {})".format(xc, yc))


if __name__ == '__main__':
    main()
