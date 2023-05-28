#!/usr/bin/env python3

import rospy
from std_msgs.msg import String
from mq7 import *
import json

mq7 = MQ7()

def read_mq7_data():
    perc = mq7.MQPercentage()
    # [perc['CO'], perc['LPG'], perc['CH4']]
    co = 2
    lpg = 3
    ch4 = 0.5
    msg = {"co":co, "lpg": lpg, "ch4": ch4}
    msg = json.dumps(msg)
    return msg

def main():
    rospy.init_node("mq7")
    pub = rospy.Publisher("gas", String, queue_size=10)
    rate = rospy.Rate(5)

    while not rospy.is_shutdown():
        msg = read_mq7_data()
        pub.publish(msg)
        #rospy.loginfo("LPG: {:f} ppm\tCO: {:f} ppm\tCH4: {:f} ppm".format(msg.data[0], msg.data[1], msg.data[2]))
        rate.sleep()



if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass