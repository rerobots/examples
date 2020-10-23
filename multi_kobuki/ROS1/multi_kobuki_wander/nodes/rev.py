#!/usr/bin/env python
"""
Copyright (C) 2020 rerobots, Inc.
This is free software, released under the Apache License, Version 2.0.
You may obtain a copy of the License at https://www.apache.org/licenses/LICENSE-2.0
"""
import time

import rospy
from geometry_msgs.msg import Twist


def main():
    movec = rospy.Publisher('mobile_base/commands/velocity', Twist, queue_size=1)
    rospy.init_node('multi_kobuki_wander')
    rate = rospy.Rate(10)
    st = time.time()
    while not rospy.is_shutdown() and time.time() - st < 10:
        m = Twist()
        m.linear.x = -.1
        movec.publish(m)
        rate.sleep()
    m = Twist()
    m.linear.x = 0
    movec.publish(m)


if __name__ == '__main__':
    main()
