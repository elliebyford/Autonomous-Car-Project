"This Module is used to control the car with PS4 DualShock Controller used for collecting data."
import MotorModule
from pyPS4Controller.controller import Controller


Motor = MotorModule

# default speed
x = 50

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_L3_up(self, value):
        Motor.forward(x)

    def on_L3_down(self, value):
        Motor.backwards(x)

    def on_L1_press(self):
        Motor.left_turn(x)

    def on_R1_press(self):
        Motor.right_turn(x)
        
    def on_R1_release(self):
        Motor.stop()
        
    def on_L1_release(self):
        Motor.stop()

    def on_L3_x_at_rest(self):
        Motor.stop()

    def on_L3_y_at_rest(self):
        Motor.stop()

controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
controller.listen()
