import cv2
import numpy
import matplotlib.pyplot as plt


def rgbToGray(image):
    b, g, r = cv2.split(image)
    image = 0.299 * r + 0.587 * g + 0.144 * r
    image = image.astype(numpy.uint8)
    return image


def rotate(image, angle):
    height, width = image.shape[:2]
    matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)
    return cv2.warpAffine(image, matrix, (width, height))


def computeHist(image):
    image = rgbToGray(image)
    height, width = image.shape[:2]
    hist = numpy.zeros(256, int)

    for i in range(0, height):
        for j in range(0, width):
            hist[image[i][j]] = hist[image[i][j]] + 1

    return hist


def binarize(image, thresh):
    image = rgbToGray(image)
    height, width = image.shape[:2]

    for i in range(0, width):
        for j in range(0, height):
            if image[i][j] < thresh:
                image[i][j] = 0
            else:
                image[i][j] = 255

    return image


def inverse(image):
    image = rgbToGray(image)
    height, width = image.shape[:2]
    I_MAX = image.max()

    for i in range(0, width):
        for j in range(0, height):
            # image[i][j] = 255 - image[i][j]
            image[i][j] = I_MAX - image[i][j]

    return image


def equalizeHist(image):
    image = rgbToGray(image)
    height, width = image.shape[:2]
    hist0 = numpy.zeros(256, int)
    for i in range(0, width):
        for j in range(0, height):
            hist0[image[i][j]] = hist0[image[i][j]] + 1

    hist0c = numpy.zeros(256, int)
    hist0c[0] = hist0[0]
    for i in range(1, 256):
        hist0c[i] = hist0[i] + hist0c[i - 1]

    nbpixels = image.size
    hist0c = hist0c / nbpixels * 255

    for i in range(0, image.shape[0]):
        for j in range(0, image.shape[1]):
            image[i][j] = hist0c[image[i][j]]

    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


def stretchHist(image, min, max):
    image = rgbToGray(image)
    height, width = image.shape[:2]

    for i in range(0, width):
        for j in range(0, height):
            image[i][j] = (255 * (image[i][j] - min)) / (max - min)

    return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)


def blur(image):
    image = rgbToGray(image)
    filter_size = 7
    filter = (1 / (filter_size * filter_size)) * numpy.ones((filter_size, filter_size), dtype=numpy.uint8)

    image1 = numpy.zeros(image.shape, dtype=numpy.uint8)

    for x in range(0, image.shape[0]):
        for y in range(0, image.shape[1]):
            width = filter.shape[0] // 2
            height = filter.shape[1] // 2
            pixel_value = 0

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - width
                    y_image = y + j - height
                    if (x_image >= 0) and (x_image < image.shape[0]) and (y_image >= 0) and (
                            y_image < image.shape[1]):
                        pixel_value += filter[i, j] * image[x_image, y_image]

            image1[x, y] = pixel_value

    return image1


def dilatation(bin_image):
    filter = numpy.ones((3, 3), dtype=numpy.uint8)
    image1 = numpy.zeros(bin_image.shape, dtype=numpy.uint8)
    for x in range(0, bin_image.shape[0]):
        for y in range(0, bin_image.shape[1]):
            width = filter.shape[0] // 2
            height = filter.shape[1] // 2
            pixel_value = 0

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - width
                    y_image = y + j - height
                    if (x_image >= 0) and (x_image < bin_image.shape[0]) and (y_image >= 0) and (
                            y_image < bin_image.shape[1]):
                        if bin_image[x_image, y_image] and filter[i, j]:
                            pixel_value = 255

            image1[x, y] = pixel_value

    return image1


def erosion(bin_image):
    filter = numpy.ones((3, 3), dtype=numpy.uint8)
    image1 = numpy.zeros(bin_image.shape, dtype=numpy.uint8)
    for x in range(0, bin_image.shape[0]):
        for y in range(0, bin_image.shape[1]):
            width = filter.shape[0] // 2
            height = filter.shape[1] // 2
            pixel_value = 255

            for i in range(0, filter.shape[0]):
                for j in range(0, filter.shape[1]):
                    x_image = x + i - width
                    y_image = y + j - height
                    if (x_image >= 0) and (x_image < bin_image.shape[0]) and (y_image >= 0) and (
                            y_image < bin_image.shape[1]):
                        if filter[i, j] and not (bin_image[x_image, y_image]):
                            pixel_value = 0

            image1[x, y] = pixel_value

    return image1


def opening(image):
    bin_image = binarize(image, 128)
    return dilatation(erosion(bin_image))


def closing(image):
    bin_image = binarize(image, 128)
    return erosion(dilatation(bin_image))


def openingTopHat(image):
    bin_image = binarize(image, 128)
    return bin_image - opening(image)


def closingTopHat(image):
    bin_image = binarize(image, 128)
    return closing(image) - bin_image


def edge(image):
    bin_image = binarize(image, 128)
    image1 = dilatation(bin_image)
    image1 = bin_image - image1
    image2 = erosion(bin_image)
    image2 = bin_image - image2

    return image1 + image2
