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

if __name__ == "__main__":

    def movingHead(q_dest):
        velma.moveHead(q_dest, 3.0, start_time=0.5)
        if velma.waitForHead() != 0:
            exitError(6)
        rospy.sleep(0.5)
        if not isHeadConfigurationClose( velma.getHeadCurrentConfiguration(), q_dest, 0.1 ):
            exitError(7)

    def movingTorso(q_map):
        velma.moveJoint(q_map, 4.0, start_time=0.5, position_tol=15.0/180.0*math.pi)
        velma.waitForJoint()
        rospy.sleep(0.5)
        js = velma.getLastJointState()
        if not isConfigurationClose(q_map, js[1], tolerance=0.1):
            exitError(10)

    q_map_starting = {'torso_0_joint':0, 'right_arm_0_joint':-0.3, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.25, 'right_arm_3_joint':0.85, 'right_arm_4_joint':0, 'right_arm_5_joint':-0.5,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':0 }
    q_map_left = {'torso_0_joint':0.7, 'right_arm_0_joint':-0.3, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.25, 'right_arm_3_joint':0.85, 'right_arm_4_joint':0, 'right_arm_5_joint':-0.5,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':0 }
    q_map_right = {'torso_0_joint':-0.7, 'right_arm_0_joint':-0.3, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.25, 'right_arm_3_joint':0.85, 'right_arm_4_joint':0, 'right_arm_5_joint':-0.5,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':0 }
    
    rospy.init_node('octomap', anonymous=False)

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

    print "Waiting for Planner initialization"
    p = Planner(velma.maxJointTrajLen())
    if not p.waitForInit(timeout_s=10.0):
        print "Could not initialize Planner"
        exitError(2)
    print "Planner initialization ok"

    print "Running octomap listener"
    oml = OctomapListener("/octomap_binary")
    rospy.sleep(1.0)
    octomap = oml.getOctomap(timeout_s=5.0)
    p.processWorld(octomap)

    print "Enabling motors"
    if velma.enableMotors() != 0:
        print "Could not enable motors"
        exitError(3)
    
    print "Switch to jnt_imp mode"
    velma.moveJointImpToCurrentPos(start_time=0.5)
    error = velma.waitForJoint()
    if error != 0:
        print "The action should have ended without error, but the error code is", error
        exitError(4)
    
    print "Checking if the starting configuration is as expected"
    rospy.sleep(0.5)
    js = velma.getLastJointState()
    if not isConfigurationClose(q_map_starting, js[1], tolerance=0.2):
        print "This test requires starting pose:"
        print q_map_starting
        exitError(10)
    print "Right configuration"
    
    print "Moving torso to left"
    movingTorso(q_map_left)
 
    rospy.sleep(1.0)

    print "Moving head to position left-zero"
    movingHead((1.56, 0))

    print "Moving head to position left-down"
    movingHead((1.56, 0.85))

    print "Moving head to position zero-down"
    movingHead((0, 0.85))

    print "Moving torso to right"
    movingTorso(q_map_right)
 
    rospy.sleep(1.0)

    print "Moving head to position right-down"
    movingHead((-1.56, 0.85))

    print "Moving head to position right-zero"
    movingHead((-1.56, 0))

    print "Moving head to position zero-zero"
    movingHead((0, 0))

    rospy.sleep(2.0)

    print "Moving torso to starting position"
    movingTorso(q_map_starting)

    rospy.sleep(2.0)
    
    exit(0)