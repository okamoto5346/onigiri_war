#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import random
from time import sleep
import copy

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

        self.old_senser_data = {}
        self.senser_data = {}
        self.sum_angle = 0
        self.sum_angle_flg = 1

        self.wheel_rot_r = 0
        self.wheel_rot_l = 0
        
        self.base_position_r = 0

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

        for i in range(0,360):
            if(i % 10 == 0):
                #print 'range %d, %d'% (i, data.ranges[i])
                self.senser_data[i] = data.ranges[i]

    def check_enemy(self):
	
        self.move_robot(0,0)
	r = rospy.Rate(5) # change speed 1fps
	for i in range(0, 5):
	    r.sleep()
	
	if len(self.senser_data) != 0:
	    for key in self.senser_data:
	   	 self.old_senser_data[key] = self.senser_data[key]
	    r.sleep()
	    is_enemy_flg = 0
	    num_count = 10
	
	    while 0 < num_count:
		total_angle = 0
	    	angle = 0
            	for data_key in self.senser_data:
	      	    if not self.senser_data[data_key] - 0.5 < self.old_senser_data[data_key] < self.senser_data[data_key] + 0.5:
			num_count = 10
			if is_enemy_flg == 0:
                            is_enemy_flg = 1
                            self.base_position_r = self.wheel_rot_r
			angle = data_key
			if angle > 180:
		    	    angle -= 180
		    	    angle = -180 + angle 
		        total_angle += angle
		angle = total_angle / 2
		if angle != 0:
	            if not -15 < angle < 15:
		        print 'angle: %d' % (angle)
		        self.turn_robot(angle)
		    for key in self.senser_data:
	   	        self.old_senser_data[key] = self.senser_data[key]
		else:
		    num_count -= 1
		
	    	r.sleep()

	    if is_enemy_flg == 1:
            	is_enemy_flg = 0
                self.revert_angle()
	

	"""
        num_count = 5
        
        r = rospy.Rate(5) # change speed 1fps
        if len(self.senser_data) != 0:
            #self.old_senser_data = self.senser_data
            for key in self.senser_data:
                self.old_senser_data[key] = self.senser_data[key]
                #print self.senser_data[key]
                #print self.old_senser_data[key]
            is_enemy_flg = 0
            while 0 < num_count:
                '''
                for i in range(0,360):
                    if(i % 10 == 0):
                        print 'range1 %d, %d'% (i, self.senser_data[i])
                        print 'range2 %d, %d'% (i, self.old_senser_data[i])
                        #self.senser_data[i] = data.ranges[i]
                '''        
                #if self.senser_data != self.old_senser_data:
                #print 'センサーデータが違います'
                angle = 0
                for data_key in self.senser_data:
                    if self.senser_data[data_key] + 0.5 <= self.old_senser_data[data_key] or self.senser_data[data_key] - 0.5 >= self.old_senser_data[data_key]:
                        if is_enemy_flg == 0:
                            is_enemy_flg = 1
                            self.base_position_r = self.wheel_rot_r
                        num_count = 5
                        if data_key >=180:
                            angle = 360 - data_key
                            angle *= -1
                        else:
                            angle = data_key
                        print 'angle: %d' % (angle)
                if angle != 0:
                    self.turn_robot(angle)
                    
                else:
                    print 'num_count %d' % (num_count)
                    num_count -= 1
		for key in self.senser_data:
                        self.old_senser_data[key] = self.senser_data[key] 
                r.sleep()
            if is_enemy_flg == 1:
                is_enemy_flg = 0
                self.revert_angle()
	"""
    def turn_robot(self, turn_angle):	# 指定した角度だけ回転する関数

	r = rospy.Rate(5)
	turn_tcount = 0

        if 0 <= turn_angle:
	    while turn_tcount < turn_angle/15:
		print '左回転'
	        self.move_robot(0,0.5)
	        turn_tcount += 1
	        r.sleep()
        else:
            while turn_tcount < turn_angle / (-10):
		print '右回転'
                self.move_robot(0,-0.5)
	        turn_tcount += 1
	        r.sleep()
	self.move_robot(0,0)
        for i in range(0, 5):
	    r.sleep()

    def revert_angle(self):

        r = rospy.Rate(5)

        while self.wheel_rot_r <= self.base_position_r - 0.2 or self.wheel_rot_r >= self.base_position_r + 0.2:
	    print '定位置に戻し中'
            if self.base_position_r < self.wheel_rot_r:
                self.move_robot(0, 0.3)
            else:
                self.move_robot(0, -0.3)
	self.move_robot(0,0)
        for i in range(0, 5):
	    r.sleep()
    
    def move_robot(self, speed, angle):
        twist = Twist()
        twist.linear.x = speed; twist.linear.y = 0; twist.linear.z = 0
        twist.angular.x = 0; twist.angular.y = 0; twist.angular.z = angle

        self.vel_pub.publish(twist)
    
    def demo_sample(self,time_count):

        #self.move_robot(0,1.0)
        #self.move_robot(0,0)
        #self.check_enemy()
        #print time_count

        #print 'wheel_r %d ' %  self.wheel_rot_r
        #print 'wheel_l %d ' %  self.wheel_rot_l

        '''
        if time_count < 10:
	    self.move_robot(0.0, 1.0)
	else:
            self.revert_angle()
	    self.move_robot(0,0)
        '''
        
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
            self.check_enemy()
	elif time_count < 109:
	    self.move_robot(-0.3,0)
	elif time_count < 116:
	    self.move_robot(0,1)
	elif time_count < 121:
	    self.move_robot(0.3,0.1)
	elif time_count < 123:
	    self.move_robot(0.15,0)
	elif time_count < 126:
	    self.move_robot(-0.15,0)
	elif time_count < 141:
	    self.move_robot(0,1)
	elif time_count < 149:
	    self.move_robot(0.4,-0.1)
	elif time_count < 151:
	    self.move_robot(0,0)
            self.check_enemy()
	elif time_count < 152:
	    self.move_robot(0,-1)
	elif time_count < 154:
	    self.move_robot(0.4,0.7)
	elif time_count < 162:
	    self.move_robot(0.4,1)
	elif time_count < 167:
	    self.move_robot(0.4,0.1)
	elif time_count < 180:
	    self.move_robot(0,1)
	elif time_count < 184:
	    self.move_robot(0.2,0)
	elif time_count < 186:
	    self.move_robot(-0.3,0)
	elif time_count < 199:
	    self.move_robot(0,-1)
	elif time_count < 206:
	    self.move_robot(0.3,0.4)
	elif time_count < 224:
	    self.move_robot(0,0)
            self.check_enemy()
       	elif time_count < 225:
	    self.move_robot(0,0.2)
        else:
            self.move_robot(0,0)
            self.check_enemy()
        
	'''
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
        '''
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
        '''
        self.wheel_rot_r = 0
        self.wheel_rot_l = 0
        '''
        #self.revert_angle()
        while not rospy.is_shutdown():
	    time_count += 1
	    self.demo_sample(time_count)
            r.sleep()
    

if __name__ == '__main__':
    rospy.init_node('ravi_mainRan')
    bot = ravi_mainRan_Bot('ravi_mainRan_bot')
    bot.strategy()
