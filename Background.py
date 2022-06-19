import numpy as np
import cv2


def detect_white_track(img):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_white = np.array([0, 0, 170])
    upper_white = np.array([179, 70, 245])
    total_white = cv2.inRange(img_hsv, lower_white, upper_white)
    return total_white


def warp_img(img, points, width, height, inv=False):
    point1 = np.float32(points)
    point2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    if inv:
        matrix = cv2.getPerspectiveTransform(point2, point1)
    else:
        matrix = cv2.getPerspectiveTransform(point1, point2)

    imgWarp = cv2.warpPerspective(img, matrix, (width, height))
    return imgWarp


def nothing(a):
    pass


def initialize_trackbars(intial_trackbar_values, wT=640, hT=480):
    cv2.namedWindow("Trackbars")
    cv2.resizeWindow("Trackbars", 480, 240)
    cv2.createTrackbar("Width Top", "Trackbars", intial_trackbar_values[0], wT // 2, nothing)
    cv2.createTrackbar("Height Top", "Trackbars", intial_trackbar_values[1], hT, nothing)
    cv2.createTrackbar("Width Bottom", "Trackbars", intial_trackbar_values[2], wT // 2, nothing)
    cv2.createTrackbar("Height Bottom", "Trackbars", intial_trackbar_values[3], hT, nothing)


def trackbar_vals(wT=640):
    width_top = cv2.getTrackbarPos("Width Top", "Trackbars")
    height_top = cv2.getTrackbarPos("Height Top", "Trackbars")
    width_bottom = cv2.getTrackbarPos("Width Bottom", "Trackbars")
    height_bottom = cv2.getTrackbarPos("Height Bottom", "Trackbars")
    points = np.float32([(width_top, height_top), (wT - width_top, height_top),
                         (width_bottom, height_bottom), (wT - width_bottom, height_bottom)])
    return points


def img_points(img, points):
    for x in range(4):
        cv2.circle(img, (int(points[x][0]), int(points[x][1])), 15, (0, 0, 255), cv2.FILLED)
    return img


def pixel_summation(img):  # was used for testing in my demos and reports.
    curve_values = np.sum(img, axis=0)
    print(curve_values)

    min_per = 1

    max_value = np.max(curve_values)
    min_value = min_per * max_value

    index_array = np.where(curve_values >= min_value)
    base_point = int(np.average(index_array))
    print(base_point)


def get_curve(img, min_per=0.1, display=False, region=1):
    if region == 1:
        curve_values = np.sum(img, axis=0)
    else:
        curve_values = np.sum(img[img.shape[0] // region:, :], axis=0)

    # print(curve_values)

    max_value = np.max(curve_values)
    min_value = min_per * max_value

    index_array = np.where(curve_values >= min_value)
    base_point = int(np.average(index_array))
    # print(base_point)

    if display:
        img_curve = np.zeros((img.shape[0], img.shape[1], 3), np.uint8)
        for x, intensity in enumerate(curve_values):
            cv2.line(img_curve, (x, img.shape[0]), (x, img.shape[0] - intensity // 255 // region), (255, 0, 255), 1)
            cv2.circle(img_curve, (base_point, img.shape[0]), 20, (0, 255, 255), cv2.FILLED)
        return base_point, img_curve
    return base_point


def combine_images(scale, img_array):  # Combination of images function i found online
    rows = len(img_array)
    cols = len(img_array[0])
    rowsAvailable = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                                                 None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale,
                                          scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        ver = hor
    return ver

