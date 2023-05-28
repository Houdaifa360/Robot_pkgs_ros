#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
import digitalio
import board
import time

ppm = [0] * 6

def pulseIn(pin):
    pulse_start = time.monotonic()
    while pin.value == False:
        pulse_start = time.monotonic()
    pulse_end = time.monotonic()
    while pin.value == True:
        pulse_end = time.monotonic()
    return pulse_end - pulse_start

ppm_pin = digitalio.DigitalInOut(board.D13)
ppm_pin.direction = digitalio.Direction.INPUT

def main():
    rospy.init_node("rc4gs")
    pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        # wait for PPM signal to start
        while ppm_pin.value == True: pass
        while ppm_pin.value == False: pass
    
        # measure the duration of each high pulse
        for i in range(len(ppm)):
            ppm[i] = pulseIn(ppm_pin)
            ppm_pin.direction = digitalio.Direction.INPUT
            time.sleep(0.001) # wait for 1ms before measuring next pulse
        
        # decode the pulse durations
        for i in range(len(ppm)):
            # rc_x = int((ppm[i] - 1.0e-3) / 2.0e-3 * 1000.0)
            rc_x = int((ppm[i] * 3.63 * 1.0e+3) - 5.26)     # Map from (1ms -> 2ms) to (-2 -> 2)
            rospy.loginfo(f"Channel {i+1}: {rc_x}")

        msg = Twist()
        msg.linear.x = rc_x
        pub.publish(msg)

        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
