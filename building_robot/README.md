# Building-robot
instrukcja<br/>

mkdir -p ~/building_ws/src<br/>
cd ~/building_ws && source /opt/ws_velma_os/setup.bash && catkin init<br/>
cd ~/building_ws/src && catkin_create_pkg building_velma std_msgs rospy geometry_msgs gazebo_msgs<br/>
cd ~/building_ws && catkin_make<br/>

source /opt/ws_velma_os/setup.bash && cd ~/building_ws && source devel/setup.bash && cd ~/building_ws/src<br/>
roslaunch building_velma velma_system.launch<br/>
roslaunch building_velma init.launch<br/>
roslaunch building_velma gazebo.launch<br/>

source /opt/ws_velma_os/setup.bash && cd ~/building_ws && source devel/setup.bash && cd ~/building_ws/src/building_velma/src/scripts<br/>
chmod +x spawn.py<br/>
rosrun building_velma spawn.py<br/>
chmod +x homologicznie.py<br/>
rosrun building_velma homologicznie.py

<br/><br/>
https://kcl-planning.github.io/ROSPlan/documentation/<br/>
https://planning.wiki/extras
