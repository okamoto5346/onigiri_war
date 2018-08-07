#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
from time import sleep

from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import JointState
from sensor_msgs.msg import LaserScan

class ravi_mainRan_Bot():
    def __init__(self, bot_name):
        # bot name 
        self.name = bot_name
        
        self.vel_pub = rospy.Publisher('cmd_vel', Twist,queue_size=1)
        # subscriber
        self.odom_sub = rospy.Subscriber('odom', Odometry, self.odomCallback)
        self.odom_sub = rospy.Subscriber('joint_states', JointState, self.jointstateCallback)
        self.lidar_sub = rospy.Subscriber('scan', LaserScan, self.lidarCallback)

    def odomCallback(self, data):
        '''
        Dont use odom in this program now
        update robot pose in gazebo
        '''
        self.pose_x = data.pose.pose.position.x
	self.pose_y = data.pose.pose.position.y

    def jointstateCallback(self, data):
        '''
        update wheel rotation num
        '''
        self.wheel_rot_r = data.position[0]
        self.wheel_rot_l = data.position[1]
	
    def lidarCallback(self, data):
        '''
        '''
	count = 300
	for i in data.intensities:
	    if((count % 10) == 0):
	    	#print '%d番目:%d' % (count, i)
		pass
	    if(count == 0):
		count = 379
            count-=1
	#print int(max(data.intensities))
	
    def move_robot(self, speed, angle):
        twist = Twist()
        twist.linear.x = speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = angle

        self.vel_pub.publish(twist)
    
    def demo_sample(self,time_count):
	if time_count < 20:
	    self.move_robot(0.35,0.5)
	elif time_count < 29:
	    self.move_robot(0,-1)
	elif time_count < 30:
	    self.move_robot(0,0)
	elif time_count < 34:
	    self.move_robot(0.1,0)
	elif time_count < 36:
	    self.move_robot(0,0)
	elif time_count < 43:
	    self.move_robot(0,-1)
	elif time_count < 62:
	    self.move_robot(0.4,0)
	elif time_count < 70:
	    self.move_robot(0,1)
	elif time_count < 71:
	    self.move_robot(0,0)
	elif time_count < 76:
	    self.move_robot(0.1,0)
	elif time_count < 77:
	    self.move_robot(0,0)
	elif time_count < 80:
	    self.move_robot(0,-1)
	elif time_count < 85:
	    self.move_robot(0.4,0.2)
	elif time_count < 101:
	    self.move_robot(0.4,0.7)
	elif time_count < 107:
	    self.move_robot(0.1,0)
	elif time_count < 108:
	    self.move_robot(0,0)
	elif time_count < 111:
	    self.move_robot(-0.3,0)
	elif time_count < 118:
	    self.move_robot(0,1)
	elif time_count < 123:
	    self.move_robot(0.3,0.1)
	elif time_count < 125:
	    self.move_robot(0.15,0)
	elif time_count < 128:
	    self.move_robot(-0.15,0)
	elif time_count < 143:
	    self.move_robot(0,1)
	elif time_count < 151:
	    self.move_robot(0.4,-0.1)
	elif time_count < 153:
	    self.move_robot(0,0)
	elif time_count < 158:
	    self.move_robot(0,-1)
	elif time_count < 162:
	    self.move_robot(0.4,0.7)
	elif time_count < 170:
	    self.move_robot(0.4,1)
	elif time_count < 175:
	    self.move_robot(0.4,0.1)
	elif time_count < 186:
	    self.move_robot(0,1)
	elif time_count < 190:
	    self.move_robot(0.2,0)
	elif time_count < 193:
	    self.move_robot(-0.3,0)
	elif time_count < 205:
	    self.move_robot(0,-1)
	elif time_count < 212:
	    self.move_robot(0.3,0.4)
	elif time_count < 230:
	    self.move_robot(0,0)
	elif time_count < 244:
	    self.move_robot(0.3,0.6)
	elif time_count < 251:
	    self.move_robot(-0.3,0.4)
	elif time_count < 255:
	    self.move_robot(0,-1)
	elif time_count < 263:
	    self.move_robot(0.3,-0.2)
	elif time_count < 270:
	    self.move_robot(0.2,0.4)
	elif time_count < 272:
	    self.move_robot(0,1)
	elif time_count < 276:
	    self.move_robot(0.1,0)
	elif time_count < 282:
	    self.move_robot(0,-1)
	elif time_count < 285:
	    self.move_robot(0.4,0.1)
	elif time_count < 295:
	    self.move_robot(0.2,0.7)
	elif time_count < 310:
	    self.move_robot(0.3,0.4)

	elif time_count < 350:
	    self.move_robot(0,0)

	elif time_count < 2000:
	    value = random.randint(1,1000)
    	    if value < 250:
                x = 0.2
                th = 0
            elif value < 500:
                x = -0.2
                th = 0
            elif value < 750:
                x = 0
                th = 1
            elif value < 1000:
                x = 0
                th = -1
            else:
                x = 0
                th = 0
 	    self.move_robot(x,th)
    def strategy(self):
        '''
        calc Twist and publish cmd_vel topic
        Go and Back loop forever
        '''
        r = rospy.Rate(5) # change speed 1fps

	'''
	時間が取れなかったため、悪あがきしています。。。。。
	申し訳ないです。m(_ _)m
	'''
	time_count = 0
        while not rospy.is_shutdown():
	    time_count += 1
	    self.demo_sample(time_count)
            r.sleep()
	

if __name__ == '__main__':
    rospy.init_node('ravi_mainRan')
    bot = ravi_mainRan_Bot('ravi_mainRan_bot')
    bot.strategy()

