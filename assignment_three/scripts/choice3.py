#! /usr/bin/env python

import rospy
import numpy
from geometry_msgs.msg import Twist, Vector3    #for cmd_vel topic
from sensor_msgs.msg import LaserScan           #for scan topic

#limit distance to avoid collision
threshold = 0.5

#initialize a Twist object for the publisher
init = Vector3(0, 0, 0)
repost = Twist( init, init)

def minimum_th(ranges):
    #function to section the ranges array in 3 parts and store the minimum distance for each of them
    
    distance= [0,0,0]
    right = ranges[0:240]
    center = ranges[240:480]
    left = ranges[480:721]
    
    distance[0] = min(right)
    distance[1] = min(center)
    distance[2] = min(left)
    return distance
        
def clbk_scan(data):
    global repost
    
    #initialize the publisher
    pub= rospy.Publisher('cmd_vel',Twist, queue_size=10)
    
    #compute the minimun obsable distance to the right, left and in front of the robot
    distances = minimum_th(data.ranges)
    if distances[0] < threshold :
        if repost.angular.z < 0 :
            #avoid turning right   
            repost.angular.z = 0    
    
    if distances[1] < threshold:
        if repost.linear.x > 0 :
            #obstacle control over user will
            repost.linear.x = 0
    
    if distances[2] < threshold :
        if repost.angular.z > 0 :
            #avoid turning left 
            repost.angular.z = 0
    
    pub.publish(repost)

def clbk_remap(data):
    #callback to copy the remap_cmd_vel on repost which can be modified or left untouched
    global repost
    repost = data
  
def inputKey_remap():
    #initialize the node
    rospy.init_node('inputKey_node')
    #subscriber to topic remap_cmd_vel    
    rospy.Subscriber("/remap_cmd_vel", Twist, clbk_remap)
    #subscriber to topic scan
    rospy.Subscriber("/scan", LaserScan, clbk_scan)
    rospy.spin()
    
#main 
if __name__=="__main__":
    inputKey_remap()
