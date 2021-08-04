#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------
#Title:  door_open_ver2のサービスサーバー
#Author:  Yusuke Kanazawa
#Data:  2021/7/28
#memo:  サービスサーバーから進行速度、入室してからの進行距離を指定できる(2DLIDER)
#-------------------------------------------------------------------------
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from door_open_ver2.srv import door_open_ver2
from door_open_ver2.srv import door_open_ver2Response

class DoorServer():
    def __init__(self):
        # サービスサーバー、パブリッシャー、サブスクライバー宣言
        rospy.Service('door_open_ver2', door_open_ver2, self.execute)
        self.pub = rospy.Publisher('/mobile_base/commands/velocity', Twist, queue_size = 10)
        rospy.Subscriber('/scan', LaserScan, self.laserCB)

    def laserCB(self, receive_msg):
        self.front_dist = receive_msg.ranges[359]

    def execute(self, req):
        try:
            MAX_linear_vel = 0.23
            MAX_target_dist = 10.0
            vel = Twist()

            #パラメーターが最大速度、最大距離以下だったらパラメーターを受け取る
            if req.linear_vel <= MAX_linear_vel and req.target_dist <= MAX_target_dist:
                vel.linear.x = req.linear_vel
                target_dist = req.target_dist

                print self.front_dist
                safe_dist = 1.0
                rospy.loginfo('start "open_door"')
                time = (req.target_dist + safe_dist) / req.linear_vel
                start_time = rospy.get_time()
                while not rospy.is_shutdown():
                    if (rospy.get_time() - start_time) <= time and self.front_dist >= safe_dist:
                         self.pub.publish(vel)
                    elif not self.front_dist >= safe_dist and (rospy.get_time() - start_time) <= time:
                        rospy.loginfo('Please open the door')
                    else:
                        pass
            return door_open_ver2Response(result = True)
        except:
            rospy.loginfo('!!Interrupted!!')
            return door_open_ver2Response(result = False)

if __name__ == '__main__':
    rospy.init_node('door_open_server')
    ds = DoorServer()
    rospy.spin()
