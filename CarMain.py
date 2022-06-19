from easygopigo3 import EasyGoPiGo3
from LaneDetection import get_lane_curve
import WebCam
import MotorModule
from time import sleep

GPG = EasyGoPiGo3()

port = "AD2"

def car_main():
    img_video = WebCam.get_video(display=False)
    curve_val = get_lane_curve(img_video, 0)

    sensitivity = 0.10  # Sensitivity for Left turns
    speed = 0.35
    if curve_val > 0:
        sensitivity = 0.10  # Sensitivity for Right turns
        if curve_val < 0.05: curve_val = 0
    else:
        if curve_val > -0.05: curve_val = 0

    total_curve = curve_val * sensitivity

    print(total_curve)

    MotorModule.move(speed, total_curve, 0.05)




if __name__ == '__main__':
    while True:
        car_main()