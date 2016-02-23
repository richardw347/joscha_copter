#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class JoystickControl():
    def __init__(self):
        self.pub = rospy.Publisher("cmd_vel", Twist, queue_size=5)
        self.twist_msg = Twist()
        self.scale = rospy.get_param("scale", 0.5)
        self.sub = rospy.Subscriber("joy", Joy, self.joy_callback)
        rate = rospy.Rate(30)
        while not rospy.is_shutdown():
            self.pub.publish(self.twist_msg)
            rate.sleep()

    def joy_callback(self, joy_msg):
        if joy_msg.buttons[11]:
            self.twist_msg.linear.x = 5.0 * joy_msg.axes[1]
            self.twist_msg.linear.y = 5.0 * joy_msg.axes[0]
            self.twist_msg.linear.z = 5.0 * joy_msg.axes[3]
            self.twist_msg.angular.z = 5.0 * joy_msg.axes[2]
        else:
            self.twist_msg.linear.x = self.scale * joy_msg.axes[1]
            self.twist_msg.linear.y = self.scale * joy_msg.axes[0]
            self.twist_msg.linear.z = self.scale * joy_msg.axes[3]
            self.twist_msg.angular.z = self.scale * joy_msg.axes[2]


if __name__ == '__main__':
    rospy.init_node("joystick_control")
    obj = JoystickControl()
