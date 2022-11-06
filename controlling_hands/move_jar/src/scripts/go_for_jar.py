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

    def movingJimp(q_map):
        goal_constraint = qMapToConstraints(q_map, 0.01, group=velma.getJointGroup("impedance_joints"))
        for i in range(10):
            rospy.sleep(0.5)
            js = velma.getLastJointState()
            print "Planning (try", i,")"
            traj = p.plan(js[1], [goal_constraint], "impedance_joints", num_planning_attempts=10, max_velocity_scaling_factor=0.05, planner_id="RRTConnect")
            if traj == None:
                continue
            print "Executing trajectory"
            if not velma.moveJointTraj(traj, start_time=0.5, position_tol=10.0/180.0 * math.pi, velocity_tol=10.0/180.0*math.pi):
                exitError(5)
            if velma.waitForJoint() == 0:
                break
            else:
                print "The trajectory could not be completed, retrying"
                continue
        rospy.sleep(0.5)

    def movingRightHand(q_dest):
        velma.moveHandRight(q_dest, [1,1,1,1], [2000,2000,2000,2000], 1000, hold=True)
        if velma.waitForHandRight() != 0:
            exitError(6)
        rospy.sleep(0.5)

    def movingCimp(T_dest):
        if not velma.moveCartImpRight([T_dest], [3.0], None, None, None, None, PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorRight() != 0:
            exitError(14)
        rospy.sleep(0.5)

    q_map_starting = {'torso_0_joint':0, 'right_arm_0_joint':-0.3, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.25, 'right_arm_3_joint':0.85, 'right_arm_4_joint':0, 'right_arm_5_joint':-0.5,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':0 }
    
    rospy.init_node('go_for_jar', anonymous=False)

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

    print "Reset right hand"
    velma.resetHandRight()
    if velma.waitForHandRight() != 0:
        exitError(2)
    rospy.sleep(0.5)
    if not isHandConfigurationClose( velma.getHandRightCurrentConfiguration(), [0,0,0,0]):
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
    
    jar = velma.getTf("B", "jar")
    jarX, jarY, jarZ = jar.p
    table = velma.getTf("B", "table")
    tableX, tableY, tableZ = table.p
    
    q_map_goal = {'torso_0_joint':math.atan2(jarY, jarX), 'right_arm_0_joint':-0.4, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.6, 'right_arm_3_joint':1.7, 'right_arm_4_joint':0.25, 'right_arm_5_joint':-1.7,
        'right_arm_6_joint':0.2, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':-0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':-0 }

    print "Closing fingers"
    movingRightHand([90.0/180.0*math.pi,90.0/180.0*math.pi,90.0/180.0*math.pi,0])
    
    print "Starting to jar"
    movingJimp(q_map_goal)
    
    print "Opening fingers"
    movingRightHand([0,0,0,0])

    rospy.sleep(0.5)

    print "Switch to cart_imp mode"
    if not velma.moveCartImpRightCurrentPos(start_time=0.2):
        exitError(8)
    if velma.waitForEffectorRight() != 0:
        exitError(9)
 
    rospy.sleep(0.5)

    print "Moving right wrist to jar"
    movingCimp(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((jarX-0.25), (jarY), (jarZ+0.1))))

    rospy.sleep(0.5)

    print "Grabbing jar"
    movingRightHand([75.0/180.0*math.pi,75.0/180.0*math.pi,75.0/180.0*math.pi,0])

    q_map_goal1 = {'torso_0_joint':math.atan2(tableY, tableX), 'right_arm_0_joint':-0.1, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.6, 'right_arm_3_joint':1.7, 'right_arm_4_joint':0.25, 'right_arm_5_joint':-1.7,
        'right_arm_6_joint':0.2, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':-0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':-0 }

    print "Switch to jnt_imp mode"
    velma.moveJointImpToCurrentPos(start_time=0.5)
    error = velma.waitForJoint()
    if error != 0:
        print "The action should have ended without error, but the error code is", error
        exitError(4)

    velma.moveJoint(q_map_goal1, 8.0, start_time=0.5, position_tol=15.0/180.0*math.pi)
    velma.waitForJoint()
    rospy.sleep(0.5)
    js = velma.getLastJointState()
    if not isConfigurationClose(q_map_goal1, js[1], tolerance=0.1):
        exitError(10)

    print "Switch to cart_imp mode"
    if not velma.moveCartImpRightCurrentPos(start_time=0.2):
        exitError(8)
    if velma.waitForEffectorRight() != 0:
        exitError(9)

    print "Moving right wrist to table"
    movingCimp(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((tableX-0.4), (tableY+0.3), (jarZ+0.3))))
    movingCimp(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((tableX-0.4), (tableY+0.3), (jarZ+0.15))))

    rospy.sleep(0.5)

    print "Leaving jar"
    movingRightHand([0,0,0,0])

    print "Moving back right wrist"
    movingCimp(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((tableX-0.7), (tableY+0.3), (jarZ+0.2))))

    rospy.sleep(0.5)

    print "Closing fingers"
    movingRightHand([90.0/180.0*math.pi,90.0/180.0*math.pi,90.0/180.0*math.pi,0])
    
    print "Switch to jnt_imp mode"
    velma.moveJointImpToCurrentPos(start_time=0.5)
    error = velma.waitForJoint()
    if error != 0:
        print "The action should have ended without error, but the error code is", error
        exitError(4)
    
    print "Moving to starting position"
    movingJimp(q_map_starting)

    print "Opening fingers"
    movingRightHand([0,0,0,0])
    
    exit(0)