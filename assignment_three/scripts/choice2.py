#! /usr/bin/env python

import rospy
from assignment_three.srv import Input_keyboard	
import os   

def manage_input(request):
    #function called by both choice 2 and 3 but if mode 3 is choosen here the launcher for that specific mode is called.
    
    if request.input_case == 1:
       #call keyboard teleop w/o obstacle avoidance
       os.system("roslaunch assignment_three choice2.launch") 
       
    elif request.input_case == 2:
        #call keyboard teleop and the osbstacle avoidance
        print("calling teleop twist keyboard with obstacle avoidance control")
        #call the launcher for case 3
        os.system("roslaunch assignment_three choice3.launch")
    else:
        print("wrong parameter")
    return 0         
   
def input_key_server():
    #node description
    
    print("driving experience node, DO NOT CLOSE THE TERMINAL")
    #initialize the node
    rospy.init_node('keyboard_controller')
    
    #call the service handler
    service = rospy.Service('input_key', Input_keyboard, manage_input)
    print("service ready")
    rospy.spin()

#main
if __name__=="__main__":
    input_key_server()
