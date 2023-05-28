#!/usr/bin/env python3

import rospy
from std_msgs.msg import Int16
import board
import digitalio

relay_pin = digitalio.DigitalInOut(board.D20)
relay_pin.direction = digitalio.Direction.OUTPUT

def turn_on():
    relay_pin.value = True

def turn_off():
    relay_pin.value = False

def callb(msg):
    status = msg.data
    if(status == 1):
        turn_on()
    elif(status == 0): 
        turn_off()


def main():
    rospy.init_node("relay_node")
    sub = rospy.Subscriber("relay", Int16, callb)
    rospy.spin()



if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass