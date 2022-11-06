#!/usr/bin/env python
import sys
import rospy

from gazebo_msgs.srv import SpawnModel, GetModelState
from geometry_msgs.msg import Pose, Point, Quaternion

if __name__ == "__main__":

    small_number = 0
    standard_number = 0
    big_number = 0

    rospy.init_node('spawn_bricks')
    rospy.wait_for_service('gazebo/spawn_sdf_model')
    spawn_model = rospy.ServiceProxy('gazebo/spawn_sdf_model', SpawnModel)
    get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)

    table = get_model_state('cafe_table', 'world')
    table_x = table.pose.position.x
    table_y = table.pose.position.y

    table0 = get_model_state('cafe_table_0', 'world')
    table0_x = table0.pose.position.x
    table0_y = table0.pose.position.y

    mid_x = (table_x+table0_x)/2
    mid_y = (table_y+table0_y)/2

    with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/small_brick/model.sdf', 'r') as brick_model:
        spawn_model('small_brick_0', brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y-0.6, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')
    with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/standard_brick/model.sdf', 'r') as brick_model:
        spawn_model('standard_brick_0', brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y-0.2, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')
    with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/big_brick/model.sdf', 'r') as brick_model:
        spawn_model('big_brick_0', brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y+0.4, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')

    small_brick_position = get_model_state('small_brick_0', 'world')
    small_brick_position_x = small_brick_position.pose.position.x
    small_brick_position_y = small_brick_position.pose.position.y
    small_brick_position_z = small_brick_position.pose.position.z

    standard_brick_position = get_model_state('standard_brick_0', 'world')
    standard_brick_position_x = standard_brick_position.pose.position.x
    standard_brick_position_y = standard_brick_position.pose.position.y
    standard_brick_position_z = standard_brick_position.pose.position.z

    big_brick_position = get_model_state('big_brick_0', 'world')
    big_brick_position_x = big_brick_position.pose.position.x
    big_brick_position_y = big_brick_position.pose.position.y
    big_brick_position_z = big_brick_position.pose.position.z

    while not rospy.is_shutdown():
        current_small_brick_position = get_model_state('small_brick_{0}'.format(small_number), 'world')
        current_small_brick_position_x = current_small_brick_position.pose.position.x
        current_small_brick_position_y = current_small_brick_position.pose.position.y
        current_small_brick_position_z = current_small_brick_position.pose.position.z
        if abs(small_brick_position_x - current_small_brick_position_x) > 0.24 or abs(small_brick_position_y - current_small_brick_position_y) > 0.24 or abs(small_brick_position_z - current_small_brick_position_z) > 0.24:
            small_number = small_number + 1
            with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/small_brick/model.sdf', 'r') as brick_model:
                spawn_model('small_brick_{0}'.format(small_number), brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y-0.6, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')

        current_standard_brick_position = get_model_state('standard_brick_{0}'.format(standard_number), 'world')
        current_standard_brick_position_x = current_standard_brick_position.pose.position.x
        current_standard_brick_position_y = current_standard_brick_position.pose.position.y
        current_standard_brick_position_z = current_standard_brick_position.pose.position.z
        if abs(standard_brick_position_x - current_standard_brick_position_x) > 0.24 or abs(standard_brick_position_y - current_standard_brick_position_y) > 0.36 or abs(standard_brick_position_z - current_standard_brick_position_z) > 0.24:
            standard_number = standard_number + 1
            with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/standard_brick/model.sdf', 'r') as brick_model:
                spawn_model('standard_brick_{0}'.format(standard_number), brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y-0.2, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')

        current_big_brick_position = get_model_state('big_brick_{0}'.format(big_number), 'world')
        current_big_brick_position_x = current_big_brick_position.pose.position.x
        current_big_brick_position_y = current_big_brick_position.pose.position.y
        current_big_brick_position_z = current_big_brick_position.pose.position.z
        if abs(big_brick_position_x - current_big_brick_position_x) > 0.24 or abs(big_brick_position_y - current_big_brick_position_y) > 0.6 or abs(big_brick_position_z - current_big_brick_position_z) > 0.24:
            big_number = big_number + 1
            with open('/home/student/building_ws/src/building_velma/src/data/gazebo/models/big_brick/model.sdf', 'r') as brick_model:
                spawn_model('big_brick_{0}'.format(big_number), brick_model.read(), '', Pose(Point(mid_x+0.3, mid_y+0.4, table.pose.position.z+0.84), Quaternion(0, 0, 0, 0)), 'world')