#!/usr/bin/env python
import roslib; roslib.load_manifest('velma_task_cs_ros_interface')
import sys
import rospy
import math
import PyKDL

from velma_common import *
from rcprg_planner import *
from rcprg_ros_utils import exitError
from control_msgs.msg import FollowJointTrajectoryResult
from geometry_msgs.msg import Twist

if __name__ == "__main__":

    def makeWrench(lx,ly,lz,rx,ry,rz):
        return PyKDL.Wrench(PyKDL.Vector(lx,ly,lz), PyKDL.Vector(rx,ry,rz))

    vel = 0.2
    time = 2/vel
    Twist msg

    rospy.init_node('kwadrat', anonymous=True)
    rospy.sleep(0.5)

    print "Running python interface for Velma"
    velma = VelmaInterface()
    print "Waiting for VelmaInterface initialization"
    if not velma.waitForInit(timeout_s=10.0):
        print "Could not initialize VelmaInterface"
        exitError(1)
    print "Initialization ok"

    diag = velma.getCoreCsDiag()
    if not diag.motorsReady():
        print "Motors must be homed and ready to use for this task"
        exitError(1)

    print "Enabling motors"
    if velma.enableMotors() != 0:
        print "Could not enable motors"
        exitError(3)

    print "Switch to cart_imp mode"
    if not velma.moveCartImpRightCurrentPos(start_time=0.2):
        exitError(8)
    if velma.waitForEffectorRight() != 0:
        exitError(9)

    if not velma.moveCartImpRight(None, None, None, None, makeWrench(1000,1000,1000,150,150,150), [0.2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.5):
        exitError(16)
    if velma.waitForEffectorRight() != 0:
        exitError(17)
    if not velma.moveCartImpLeft(None, None, None, None, makeWrench(1000,1000,1000,150,150,150), [0.2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.5):
        exitError(16)
    if velma.waitForEffectorLeft() != 0:
        exitError(17)

    pub = rospy.Publisher('mux_vel_nav', Twist, queue_size=10)
    
    msg.angular.x = 0
    msg.angular.y = 0
    msg.angular.z = 0
    msg.linear.x = vel
    msg.linear.y = 0
    msg.linear.z = 0
    pub.publish(msg)
    sleep(time)

    msg.linear.x = 0
    msg.linear.y = vel
    pub.publish(msg)
    sleep(time)

    msg.linear.x = -vel
    msg.linear.y = 0
    pub.publish(msg)
    sleep(time)

    msg.linear.x = 0
    msg.linear.y = -vel
    pub.publish(msg)
    sleep(time)
    
    msg.linear.x = 0
    msg.linear.y = 0
    pub.publish(msg)
    sleep(0.5)

    exit(0)