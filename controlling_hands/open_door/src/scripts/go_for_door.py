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
        velma.moveJoint(q_map, 4.0, start_time=0.5, position_tol=15.0/180.0*math.pi)
        velma.waitForJoint()
        rospy.sleep(0.5)
        js = velma.getLastJointState()
        if not isConfigurationClose(q_map, js[1], tolerance=0.1):
            exitError(10)

    def movingCimpRight(T_dest):
        imp_list = [makeWrench(70,70,70,50,50,50)]
        if not velma.moveCartImpRight([T_dest], [3.0], None, None, imp_list, [2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorRight() != 0:
            exitError(14)
        rospy.sleep(0.5)

    def open(T_dest):
        imp_list = [makeWrench(300,300,300,75,75,75)]
        if not velma.moveCartImpRight([T_dest], [3.0], None, None, imp_list, [2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorRight() != 0:
            exitError(14)
        rospy.sleep(0.5)

    def movingCimpLeft(T_dest):
        if not velma.moveCartImpLeft([T_dest], [3.0], None, None, None, None, PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorLeft() != 0:
            exitError(14)
        rospy.sleep(0.5)

    def movingRightHand(q_dest):
        velma.moveHandRight(q_dest, [1,1,1,1], [2000,2000,2000,2000], 1000, hold=True)
        if velma.waitForHandRight() != 0:
            exitError(6)
        rospy.sleep(0.5)

    def makeWrench(lx,ly,lz,rx,ry,rz):
        return PyKDL.Wrench(PyKDL.Vector(lx,ly,lz), PyKDL.Vector(rx,ry,rz))

    q_map_starting = {'torso_0_joint':0, 'right_arm_0_joint':-0.3, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.25, 'right_arm_3_joint':0.85, 'right_arm_4_joint':0, 'right_arm_5_joint':-0.5,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.3, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.25,
        'left_arm_3_joint':-0.85, 'left_arm_4_joint':0, 'left_arm_5_joint':0.5, 'left_arm_6_joint':0 }

    rospy.init_node('go_for_door', anonymous=False)

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

    board = velma.getTf("B", "board")
    boardX, boardY, boardZ = board.p
    alpha = math.atan2(boardY, boardX)
    i = 0.4
    j = 0.07
    q_map_goal = {'torso_0_joint':alpha, 'right_arm_0_joint':-0.4, 'right_arm_1_joint':-1.8,
        'right_arm_2_joint':1.6, 'right_arm_3_joint':1.7, 'right_arm_4_joint':0.25, 'right_arm_5_joint':-1.7,
        'right_arm_6_joint':0, 'left_arm_0_joint':0.4, 'left_arm_1_joint':1.8, 'left_arm_2_joint':-1.6,
        'left_arm_3_joint':-1.7, 'left_arm_4_joint':0.25, 'left_arm_5_joint':1.7, 'left_arm_6_joint':0 }
    
    print "Moving to board"
    movingJimp(q_map_goal)

    print "Preparing hand"
    movingRightHand([0.6*math.pi,0.6*math.pi,0.6*math.pi,math.pi])

    print "Switch to cart_imp mode"
    if not velma.moveCartImpRightCurrentPos(start_time=0.2):
        exitError(8)
    if velma.waitForEffectorRight() != 0:
        exitError(9)

    print "Finding door"
    while velma.waitForEffectorRight() == 0:
        i = i - 0.02
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-i), (boardY-j), (boardZ+0.11))))
        T_B_T_diff = PyKDL.diff(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-i), (boardY-j), (boardZ+0.11))), velma.getTf("B", "Tr"), 1.0)
        if T_B_T_diff.vel.Norm() > 0.05 or T_B_T_diff.rot.Norm() > 0.05:
            break
    print "Door found"
    rospy.sleep(0.5)

    print "Finding handle"
    while velma.waitForEffectorRight() == 0:
        j = j - 0.02
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-(i+0.02)), (boardY-j), (boardZ+0.11))))
        T_B_T_diff = PyKDL.diff(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-i), (boardY-j), (boardZ+0.11))), velma.getTf("B", "Tr"), 1.0)
        if T_B_T_diff.vel.Norm() > 0.04 or T_B_T_diff.rot.Norm() > 0.04:
            break
    print "Handle found"
    rospy.sleep(0.5)

    print "Opening door with right hand"
    movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-(i+0.025)), (boardY-j)-0.036, (boardZ+0.11))))
    open(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-0.55), (boardY-0.05), (boardZ+0.11))))
    rospy.sleep(0.5)
    open(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-0.65), (boardY-0.15), (boardZ+0.11))))
    rospy.sleep(0.5)

    print "Hiding right hand"
    movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-0.45), (boardY-0.4), (boardZ+0.11))))
    rospy.sleep(0.5)
    movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RotZ(alpha), PyKDL.Vector((boardX-0.9), (boardY-0.6), (boardZ-0.1))))
    rospy.sleep(0.5)

    print "Opening door with left hand"
    movingCimpLeft(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((boardX-0.25), (boardY), (boardZ+0.3))))
    rospy.sleep(0.5)
    movingCimpLeft(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((boardX-0.3), (boardY-0.25), (boardZ+0.3))))
    rospy.sleep(0.5)

    print "Hiding left hand"
    movingCimpLeft(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((boardX-0.35), (boardY+0.4), (boardZ+0.3))))
    rospy.sleep(0.5)
    movingCimpLeft(PyKDL.Frame(PyKDL.Rotation.Quaternion(0.0, 0.0, 0.0, 1.0), PyKDL.Vector((boardX-0.6), (boardY+0.4), (boardZ+0.3))))
    rospy.sleep(0.5)

    print "Switch to jnt_imp mode"
    velma.moveJointImpToCurrentPos(start_time=0.5)
    error = velma.waitForJoint()
    if error != 0:
        print "The action should have ended without error, but the error code is", error
        exitError(4)

    print "Opening hand"
    movingRightHand([0,0,0,0])

    print "Moving to starting position"
    movingJimp(q_map_starting)

    rospy.sleep(0.5)
    
    exit(0)