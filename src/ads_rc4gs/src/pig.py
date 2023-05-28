# <sudo apt-get install pigpio>
# <sudo pigpiod>
import rospy
from geometry_msgs.msg import Twist
import pigpio

servo_min = -2
servo_max = 2
ch1 = 18
ch2 = 23
freq = 50
servo_value_linear = 0.0  
servo_value_angular = 0.0  

rospy.init_node("rc4gs")
pub = rospy.Publisher("cmd_vel", Twist, queue_size=10)
rate = rospy.Rate(10)

def map_pulse_width_to_servo_value(pulse_width):
    pulse_min = 1000  # 1ms = 1000 microseconds
    pulse_max = 2000  # 2ms = 2000 microseconds

    # Map the pulse width to the servo value range
    servo_value = ((pulse_width - pulse_min) * (servo_max - servo_min) / (pulse_max - pulse_min)) + servo_min
    if(servo_value > servo_max): servo_value = servo_max
    if(servo_value < servo_min): servo_value = servo_min

    if(servo_value < 0.2 and servo_value > -0.2):
        servo_value = 0

    return servo_value

def rc_callback2(gpio, level, tick):
    global start_tick_2
    global servo_value_linear
    if level == 1:
        start_tick_2 = tick
    else:
        pulse_width = tick - start_tick_2
        servo_value_linear = map_pulse_width_to_servo_value(pulse_width)

def rc_callback1(gpio, level, tick):
    global start_tick_1
    global servo_value_angular
    if level == 1:
        start_tick_1 = tick
    else:
        pulse_width = tick - start_tick_1
        servo_value_angular = map_pulse_width_to_servo_value(pulse_width)

pi = pigpio.pi()
# Throttle Channel
pi.set_mode(ch2, pigpio.INPUT)
pi.set_pull_up_down(ch2, pigpio.PUD_UP)
pi.set_PWM_frequency(ch2, freq)
pi.callback(ch2, pigpio.EITHER_EDGE, rc_callback2)

# Steering Channel
pi.set_mode(ch1, pigpio.INPUT)
pi.set_pull_up_down(ch1, pigpio.PUD_UP)
pi.set_PWM_frequency(ch1, freq)
pi.callback(ch1, pigpio.EITHER_EDGE, rc_callback1)

def main():
    while not rospy.is_shutdown():
        msg = Twist()
        msg.linear.x = servo_value_linear
        msg.angular.z = servo_value_angular
        pub.publish(msg)
        rospy.loginfo(f"value {msg}")
        rate.sleep()


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
