#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import json

i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P2)

def read_pot_val():
    temp = 25
    msg = {"temp": temp}
    msg = json.dumps(msg)
    return msg

def main():
    rospy.init_node("temp_node")
    pub = rospy.Publisher("temp", String, queue_size=10)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        msg = read_pot_val()
        pub.publish(msg)
        rate.sleep()



if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass