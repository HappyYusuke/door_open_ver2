#!/usr/bin/env python
# -*- coding: utf-8 -*-
#------------------------------------------------------------
#Title: door_open_ver2のサービスクライアント
#Author: Kanazawa Yusuke
#Data: 2021/7/27
#memo:
#------------------------------------------------------------
import rospy
from geometry_msgs.msg import Twist
from door_open_ver2.srv  import door_open_ver2
import sys

if __name__ == '__main__':
    rospy.init_node('door_opne_client')
    set_value = rospy.ServiceProxy('door_open_ver2', door_open_ver2)
    linear_vel = float(sys.argv[1]) #sys.argvはコマンドラインからの引数を扱う
    target_dist = float(sys.argv[2])
    response = set_value(linear_vel, target_dist)
    if response.result:
        rospy.loginfo('set [%f, %f] success' % (linear_vel, target_dist))
    else:
        rospy.loginfo('set [%f, %f] failed' % (linear_vel, target_dist))
