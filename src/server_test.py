#!/usr/bin/env python
# -*- coding: utf-8 -*-
#----------------------------------------------------------------------
#Title:　door_open_ver2のサービスサーバ
#Author:　Kanazawa Yusuke
#Data:　2021/7/2
#memo:　サービスサーバーから進行速度、入室してからの進行距離を指定できる
#----------------------------------------------------------------------
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from door_open_ver2.srv import door_open_ver2
from door_open_ver2.srv import door_open_ver2Response

MAX_LINER_VELOCITY = 0.23
MIN_LINER_VELOCITY = 0.0
MAX_PROCRESS_DISTANCE = 10.0
MIN_PROGRESS_DISTANCE = 0.0

def value_set(request):
    vel = Twist()
    is_set_success = True

    if request.linear_vel <= MAX_LINER_VELOCITY and (request.linear_vel >= MIN_LINER_VELOCITY):
        vel.linear.x = request.linear_vel
    else:
        is_set_success = False
    if request.target_dist <= MAX_PROCRESS_DISTANCE and (request.target_dist >= MIN_PROGRESS_DISTANCE):
        target_dist = request.target_dist
    else:
        is_set_success = False

    if is_set_success:
        time = request.target_dist / request.linear_vel
        start_time = rospy.get_time()
        while not rospy.is_shutdown() and (rospy.get_time() - start_time) <= time:
            print('now_time = ', rospy.get_time() - start_time)
            pub.publish(vel)
    return door_open_ver2Response(result = is_set_success)

if __name__ == '__main__':
    rospy.init_node('door_open_server_test')
    pub = rospy.Publisher('/mobile_base/commands/velocity',Twist, queue_size = 10)
    service_server = rospy.Service('door_open_ver2', door_open_ver2, value_set)
    rospy.spin()
