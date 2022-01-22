#! /usr/bin/env python

import rospy
from assignment_three.srv import Directions		#service for mode 1
from assignment_three.srv import Input_keyboard	#service for mode 2 and 3


def userInterface():
    #function to explain the user how to use the program
    #returns the input form the user to send them to the menage service
    
    print("Hello User! please select between the different modalities:")
    print("1) automatic reach of the coordinates chosen by you")
    print("2) driving a robot experience")
    print("3) learn to drive, collision handler active")
    print("0) quit")
    print()        
    return input("input your choice: ")

def choice1():
    #function to handle mode 1: takes the coordinates form the user and checks if the aimed target is reached
    #calls the service Directions and sends the coordinates to the manage_input(request) function in choice1.py
    
    print("mode 1")
    x = float(input("insert x: "))
    y = float(input("insert y: "))
    
    rospy.wait_for_service('directions')
    directions = rospy.ServiceProxy('directions', Directions)
    aim= directions(x , y)
    
    if aim.return_== 1:
    	print("target reached successfully!")
    else:
    	print("target not reached")

#call the keyboard service to handle the case           	
def choice2():
    #function to handle mode 2: calls the service to manage the input from keyboard
    #if the user selects mode 2 it will send 1 to the manage_input(request) function in choice2.py
    
    print("mode 2")
    rospy.wait_for_service('input_key')
    usrInput = rospy.ServiceProxy('input_key', Input_keyboard)
    usrInput(1)

def choice3():
    #function to handle mode 3: calls the service to manage the input from keyboard
    #if the user selects mode 3 it will send 2 to the manage_input(request) function in choice2.py
    
    print("choice 3")
    rospy.wait_for_service('input_key')
    usrInput = rospy.ServiceProxy('input_key', Input_keyboard)
    usrInput(2)


 
if __name__=="__main__":
    #initialize the ros node
    rospy.init_node('main_controller')
    flag = 1
    
    while(flag):
        #loop to print the interface and save the choice in the varible mode
        
        mode = userInterface()
        
        if mode.isnumeric():
            mode = int(mode)
            if (mode == 1):
                choice1()
            
            elif (mode == 2):
                choice2()  
            
            elif (mode == 3):
                choice3()
            
            elif (mode == 0):
                flag = 0
                print("press ctrl-C to quit")
                print()
            
            else:
                print("incorrect input!!")
        else:
            print("input value is not a number!!")
