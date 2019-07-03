#!/usr/bin/env python
import rospy
from eps_control.msg import Steer
from eps import EPS

eps_driver = None

def steer_callback(msg):

    eps_driver.set_steering_angle(msg.steer)

if __name__ == '__main__':

    rospy.init_node('eps_control_python_node', anonymous=True)

    port = rospy.get_param('~port',default='/dev/ttyUSB0')
    baud_rate = rospy.get_param('~baud_rate', default=300000)
    steering_rate = rospy.get_param('~steering_rate', default=10)
    telemetry_period = rospy.get_param('~telemetry_period', default=0.2)
    max_angle = rospy.get_param('~max_steering_angle', default=32)
    max_eps_position = rospy.get_param('~max_eps_position', default=1500)
    middle_eps_position = rospy.get_param('~middle_eps_position', default=1000)


    eps_driver = EPS(port, baud_rate, 
                     steering_rate, telemetry_period,
                     max_angle, max_eps_position, middle_eps_position)

    eps_driver.start()

    rospy.Subscriber('cmd_steer', Steer, steer_callback,  queue_size=1)

    rospy.spin()

    eps_driver.stop()