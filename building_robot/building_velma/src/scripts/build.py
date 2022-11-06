#!/usr/bin/env python
import roslib; roslib.load_manifest('velma_task_cs_ros_interface')
import sys
import rospy
import math
import PyKDL
import time

from velma_common import *
from rcprg_planner import *
from rcprg_ros_utils import exitError
from geometry_msgs.msg import Twist

if __name__ == "__main__":

    vel = 0.2
    table_length = 0.913
    length_from_table = 0.6
    length_from_brick = length_from_table-0.3
    msg = Twist()
    q_map_starting = {'torso_0_joint':0, 'right_arm_0_joint':0.7, 'right_arm_1_joint':-1.7,
        'right_arm_2_joint':1.75, 'right_arm_3_joint':1.1, 'right_arm_4_joint':0.25, 'right_arm_5_joint':0.1,
        'right_arm_6_joint':0, 'left_arm_0_joint':-0.7, 'left_arm_1_joint':1.7, 'left_arm_2_joint':-1.75,
        'left_arm_3_joint':-1.1, 'left_arm_4_joint':-0.25, 'left_arm_5_joint':-0.1, 'left_arm_6_joint':0 }

    def makeWrench(lx,ly,lz,rx,ry,rz):
        return PyKDL.Wrench(PyKDL.Vector(lx,ly,lz), PyKDL.Vector(rx,ry,rz))

    def countTime(vel, s):
        if vel<0:
            vel=-vel
        if s<0:
            s=-s
        if vel==0:
            return 0
        else:
            return s/vel

    def switchToJimp():
        print "Switch to jnt_imp mode"
        velma.moveJointImpToCurrentPos(start_time=0.5)
        error = velma.waitForJoint()
        if error != 0:
            print "The action should have ended without error, but the error code is", error
            exitError(4)
        rospy.sleep(0.5)

    def switchToCimp():
        print "Switch to cart_imp mode"
        if not velma.moveCartImpRightCurrentPos(start_time=0.2):
            exitError(8)
        if velma.waitForEffectorRight() != 0:
            exitError(9)
        if not velma.moveCartImpLeftCurrentPos(start_time=0.2):
            exitError(10)
        if velma.waitForEffectorLeft() != 0:
            exitError(11)
        rospy.sleep(0.5)

    def movingJimp(q_map):
        velma.moveJoint(q_map, 4.0, start_time=0.5, position_tol=15.0/180.0*math.pi)
        velma.waitForJoint()
        rospy.sleep(0.5)
        js = velma.getLastJointState()
        if not isConfigurationClose(q_map, js[1], tolerance=0.1):
            exitError(10)
        rospy.sleep(0.5)

    def movingCimpRight(T_dest):
        if not velma.moveCartImpRight([T_dest], [3.0], None, None, [makeWrench(700,700,700,500,500,500)], [2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorRight() != 0:
            exitError(14)
        rospy.sleep(0.5)

    def movingCimpLeft(T_dest):
        if not velma.moveCartImpLeft([T_dest], [3.0], None, None, [makeWrench(700,700,700,500,500,500)], [2], PyKDL.Wrench(PyKDL.Vector(5,5,5), PyKDL.Vector(5,5,5)), start_time=0.2):
            exitError(13)
        if velma.waitForEffectorLeft() != 0:
            exitError(14)
        rospy.sleep(0.5)

    def movingRightHand(q_dest):
        velma.moveHandRight(q_dest, [1,1,1,1], [2000,2000,2000,2000], 1000, hold=True)
        if velma.waitForHandRight() != 0:
            exitError(6)
        rospy.sleep(0.5)

    def movingLeftHand(q_dest):
        velma.moveHandLeft(q_dest, [1,1,1,1], [2000,2000,2000,2000], 1000, hold=True)
        if velma.waitForHandLeft() != 0:
            exitError(6)
        rospy.sleep(0.5)

    def moveForward(s, vel=vel, length=0):
        if s<0:
            s = -s
            s = s - length
        if s>0:
            s = s - length
        msg.linear.x = vel
        msg.linear.y = 0
        msg.angular.z = 0
        pub.publish(msg)
        rospy.sleep(countTime(vel=vel, s=s))

    def moveAside(s,vel=vel):
        msg.linear.x = 0
        if s>0:
            msg.linear.y = vel
        if s<0:
            msg.linear.y = -vel
        msg.angular.z = 0
        pub.publish(msg)
        rospy.sleep(countTime(vel=vel, s=s))

    def moveAround(s, vel=vel):
        msg.linear.x = 0
        msg.linear.y = 0
        msg.angular.z = vel
        pub.publish(msg)
        rospy.sleep(countTime(vel=vel, s=s))

    def stopMoving():
        msg.angular.x = 0
        msg.angular.y = 0
        msg.angular.z = 0
        msg.linear.x = 0
        msg.linear.y = 0
        msg.linear.z = 0
        pub.publish(msg)
        rospy.sleep(0.5)

    def movingForSmallBrick():
        #moveAside(vel=-vel, s=small_brick_y)
        #moveForward(s=small_brick_x, length=length_from_brick)
        stopMoving()
        #tu podnoszenie
        switchToCimp()
        movingRightHand([0,0,0,0])
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RPY(math.pi*3/2, math.pi/2, 0), PyKDL.Vector(0.715, 0.115, 1.3)))
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RPY(math.pi*3/2, math.pi/2, 0), PyKDL.Vector(0.715, 0.115, 1.15)))
        movingRightHand([65.0/180.0*math.pi,65.0/180.0*math.pi,65.0/180.0*math.pi,0])
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RPY(math.pi*3/2, math.pi/2, 0), PyKDL.Vector(0.715, 0.115, 1.4)))

        #odkladanie
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RPY(math.pi*3/2, math.pi/2, 0), PyKDL.Vector(0.715, 0.115, 1.155)))
        movingRightHand([0,0,0,0])
        movingCimpRight(PyKDL.Frame(PyKDL.Rotation.RPY(math.pi*3/2, math.pi/2, 0), PyKDL.Vector(0.715, 0.115, 1.3)))
        #moveForward(s=small_brick_x, vel=-vel, length=length_from_brick)
        #moveAround(vel=-vel, s=math.pi)
        #moveAside(vel=-vel, s=small_brick_y)

    def movingForStandardBrick():
        moveAside(vel=-vel, s=standard_brick_y)
        moveForward(s=standard_brick_x, length=length_from_brick)
        #tu podnoszenie
        moveForward(s=standard_brick_x, vel=-vel, length=length_from_brick)
        moveAround(vel=-vel, s=math.pi)
        moveAside(vel=-vel, s=standard_brick_y)

    def movingForBigBrick():
        moveAside(vel=-vel, s=big_brick_y)
        moveForward(s=big_brick_x, length=length_from_brick)
        #tu podnoszenie
        moveForward(s=big_brick_x, vel=-vel, length=length_from_brick)
        moveAround(vel=-vel, s=math.pi)
        moveAside(vel=-vel, s=big_brick_y)

    def movingSouth():
        moveAside(s=mid_y)
        moveForward(s=mid_x, length=length_from_table+table_length)
        #tu odkladanie
        moveForward(s=mid_x, vel=-vel, length=length_from_table+table_length)
        moveAround(vel=-vel, s=math.pi)
        moveAside(s=mid_y)

    def movingEast():
        moveAside(s=mid_y-(2*table_length))
        moveForward(s=mid_x)
        moveAround(s=math.pi/2)
        moveForward(s=2*table_length, length=length_from_table+table_length)
        #tu odkladanie
        moveForward(s=2*table_length, vel=-vel, length=length_from_table+table_length)
        moveAround(s=math.pi/2)
        moveForward(s=mid_x)
        moveAside(s=mid_y-(2*table_length))

    def movingWest():
        moveAside(s=mid_y+(2*table_length))
        moveForward(s=mid_x)
        moveAround(vel=-vel, s=math.pi/2)
        moveForward(s=2*table_length, length=length_from_table+table_length)
        #tu odkladanie
        moveForward(s=2*table_length, vel=-vel, length=length_from_table+table_length)
        moveAround(vel=-vel, s=math.pi/2)
        moveForward(s=mid_x)
        moveAside(s=mid_y+(2*table_length))

    def movingNorth():
        moveAside(s=mid_y+(2*table_length))
        moveForward(s=mid_x+(2*table_length))
        moveAround(vel=-vel, s=math.pi/2)
        moveForward(s=2*table_length)
        moveAround(vel=-vel, s=math.pi/2)
        moveForward(s=2*table_length, length=length_from_table+table_length)
        #tu odkladanie
        moveForward(s=2*table_length, vel=-vel, length=length_from_table+table_length)
        moveAround(s=math.pi/2)
        moveForward(s=2*table_length)
        moveAround(vel=-vel, s=math.pi/2)
        moveForward(s=mid_x+(2*table_length))
        moveAside(s=mid_y-(2*table_length))
    
    rospy.init_node('testy', anonymous=True)
    pub = rospy.Publisher('mux_vel_nav/cmd_vel', Twist, queue_size=10)

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
    rospy.sleep(0.5)

    table = velma.getTf("B", "table")
    table_x, table_y, table_z = table.p
    table = velma.getTf("B", "table_0")
    table0_x, table0_y, table0_z = table.p
    table = velma.getTf("B", "table_1")
    table1_x, table1_y, table1_z = table.p
    table = velma.getTf("B", "table_2")
    table2_x, table2_y, table2_z = table.p
    table = velma.getTf("B", "table_3")
    table3_x, table3_y, table3_z = table.p
    table = velma.getTf("B", "table_4")
    table4_x, table4_y, table4_z = table.p

    mid_x = (table_x+table0_x)/2
    mid_y = (table_y+table0_y)/2
    small_brick_x = mid_x+0.3
    small_brick_y = mid_y-0.6
    standard_brick_x = mid_x+0.3
    standard_brick_y = mid_y-0.2
    big_brick_x = mid_x+0.3
    big_brick_y = mid_y+0.4

    mid_x = (table1_x+table4_x)/2+0.2
    mid_y = (table1_y+table4_y)/2
    first_brick_x = mid_x-0.72
    first_brick_y = mid_y+0.72

    #switchToJimp()
    #movingJimp(q_map_starting)
    stopMoving()
    #moveAround(vel=-vel, s=math.pi)

    #movingEast()
    movingForSmallBrick()
    #movingSouth()
    #movingForStandardBrick()
    #movingWest()
    #movingForBigBrick()
    #movingNorth()
    stopMoving()

    exit(0)