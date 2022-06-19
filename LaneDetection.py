import numpy as np
import cv2
import Background

bck = Background

curve_list = []
avg_val = 10


def get_lane_curve(img, display=2):
    initial_trackbar_vals = [110, 395, 90, 451]  # Where you enter the Morph Values
    bck.initialize_trackbars(initial_trackbar_vals)  # Sends the Morph Values to Background to initialize

    img_copy = img.copy()
    img_result = img.copy()
    img_lane = bck.detect_white_track(img)  # Lane detection (Seperates lane from rest of image)

    height, width, c = img.shape
    points = bck.trackbar_vals()

    # Warping step
    img_warp = bck.warp_img(img_lane, points, width, height)
    img_warp_points = bck.img_points(img_copy, points)

    # Curve Detection Step
    mid_point, img_curve = bck.get_curve(img_warp, display=True, min_per=0.5, region=4)
    curve_avg_point, img_curve = bck.get_curve(img_warp, display=True, min_per=0.9)
    curve_raw = curve_avg_point - mid_point

    # Averaging
    curve_list.append(curve_raw)
    if len(curve_list) > avg_val:
        curve_list.pop(0)

    curve = int(sum(curve_list) / len(curve_list))

    # Display, img_lane_colour

    if display == 1:
        img_inv_warp = bck.warp_img(img_warp, points, width, height, inv=True)
        img_inv_warp = cv2.cvtColor(img_inv_warp, cv2.COLOR_GRAY2BGR)
        img_inv_warp[0:height // 3, 0:width] = 0, 0, 0
        img_lane_colour = np.zeros_like(img)
        img_lane_colour[:] = 0, 255, 0
        img_lane_colour = cv2.bitwise_and(img_inv_warp, img_lane_colour)

        combined_images = bck.combine_images(0.7, ([img, img_warp_points, img_warp],
                                                   [img_curve, img_lane_colour, img_lane]))
        cv2.imshow('Combined Images', combined_images)

    #### DEBUGGING SPECIFIC FUNCTIONS ###

    # cv2.imshow('Lane', img_lane)  # Displays the detected lane in white

    # cv2.imshow('Warp Points', img_warp_points)  # creates copy of video with points on it

    # cv2.imshow('Warp', img_warp)     #Actually Warps the image (displays the outcome of the warping

    # bck.pixel_summation(img_warp)

    # cv2.imshow('Image Curve', img_curve)

    # bck.get_curve(img_warp)

    # print(basePoint-mid_point)

    ### FINAL RETURN of CURVE ###

    curve = curve / 100

    # print(curve)

    return curve


if __name__ == '__main__':
    # cap = cv2.VideoCapture('home/pi/Desktop/Project/vidNewHeight1.mp4')
    cap = cv2.VideoCapture(0)
    initial_trackbar_vals = [110, 400, 90, 451]
    bck.initialize_trackbars(initial_trackbar_vals)
    frame_counter = 0
    curve_list = []
    while True:
        frame_counter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frame_counter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frame_counter = 0

        success, img = cap.read()  # GET THE IMAGE
        img = cv2.resize(img, (640, 480))  # RESIZE
        lane_curve = get_lane_curve(img, display=2)
        # print(curve)

        # cv2.imshow('vid', img) #displays original video

        cv2.waitKey(10)

# cap.release()
# cv2.destroyAllWindows()