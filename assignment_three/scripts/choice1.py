#! /usr/bin/env python

import rospy
from assignment_three.srv import Directions 
# import fo the action
import actionlib
from move_base_msgs.msg import *
from actionlib_msgs.msg import *
 
def manage_input(request):
    #function to manage the user choice of mode 1. Sets the target and waits for the result
    
    x = request.x
    y = request.y
    print("going to point x: ",x," y: ",y)
    
    #starting the action and wait for the server 
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()
    target = MoveBaseGoal()
    
    #set the target's parameters
    target.target_pose.header.frame_id = 'map'
    target.target_pose.pose.orientation.w = 1
    target.target_pose.pose.position.x = x
    target.target_pose.pose.position.y = y
    
    #send the target
    client.send_goal(target)
    #timeout to prevent infinite waiting
    wait = client.wait_for_result(timeout=rospy.Duration(50.0))
    
    if not wait:
        #target not reached
        print("the point can't be reached!")
        client.cancel_goal()
        return -1
    #target reached
    print("Arrived at destination")
    return 1

def directions_server():
    #node description
    
    print("automatic motion node, DO NOT CLOSE THE TERMINAL")
    #initialize the node
    rospy.init_node('directions_controller')
    
    #call the service handler
    s = rospy.Service('directions', Directions, manage_input)
    print("service ready")
    rospy.spin()

if __name__=="__main__":
    directions_server() 
