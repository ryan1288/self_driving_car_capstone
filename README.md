# Self-driving Car Capstone
---
The goals / steps of this project are the following:
* Implement a system using ROS that provide the full functionality of an autonomous vehicle.
* Understand the system architecture and node interactions
* Work on the perception, planning, and control module
* Use the simulator to test the interactions in the self-driving car
* Summarize the results with a written report

[//]: # (Image References)

[image1]: report_images/system.png
[image2]: report_images/Sim1.JPG
[image3]: report_images/Sim2.JPG
[image4]: report_images/tl_detector.png
[image5]: report_images/waypoint_updater.png
[image6]: report_images/twist_controller.png

---
## Project Overview
This project utilizes `rospy`, the python client for ROS to quickly interface with ROS nodes, services, parameters, etc.

I worked on the named python files below in this capstone project. The remainder of the work was from Udacity.
1. Perception Module
   * Traffic Light Detection Node (`tl_detector.py` and `tl_classifier.py`)
2. Planning Module
   * Waypoint Loader
   * Waypoint Updater Node (`waypoint_updater.py`)
3. Control Module
   * DBW Node (`dbw_node.py` and `twist_controller.py`)
   * Waypoint Follower

## System Architecture:

![][image1]

In the nodes below, the diagrams show the topics that the node is subscribed or publishes to.

### Waypoint Updater Node
The node is initialized with the full list of original waypoints. Subscribed to a continuous stream of the current vehicle position and next red traffic light position, it will make the car drive either normally or decelerate (if the traffic light is near). An efficient look-up uses the KDTree data structure for the index of the next waypoint.

A square root shape function is currently used to slow down the vehicle as it approaches the stop line (published to /final_waypoints).

![][image5]

### DBW Node
I implemented the control in two different scripts. The `twist_controller.py` has the yaw, throttle, and brake PID control. It also uses the motion model of the car to predict the required braking force to stop.

* Steering - implemented in the YawController class `yaw_controller.py`
* Throttle - [Speed Control Algorithm](https://ijssst.info/Vol-17/No-30/paper19.pdf) that uses the squared difference in velocity (current and target) for a smooth transition to the reference velocity
* Brake - negative throttle depends on the vehicle's mass and wheel radius (motion model) 

![][image6]

### Traffic Light Detection Node
In `tl_classifier.py`, the model used Tensorflow-GPU 1.3 and Keras, trained on the desktop and uses the TensorFlow Object Detection API ([Reference1](https://medium.com/@WuStangDan/step-by-step-tensorflow-object-detection-api-tutorial-part-1-selecting-a-model-a02b6aabe39e) and [Reference2](https://github.com/alex-lechner/Traffic-Light-Classification) when learning) to re-train Several hundred images were used, utilizing labels provided by `/vehicle/traffic_lights` topic (accurate labels from the simulator).

![][image4]

The SSD Inception V2 Coco was used as the base model and the last layer was resized and retrained to the data set from the traffic lights in the simulator. Although the system architecture does not make use of whether the detected color is green or yellow, it was included in the model for generalization. A TFRecord was generated to train the model after labelling using labellmg.

Four possible classification outputs:
* Green Light (ID = 1)
* Red Light (ID = 2)
* Yellow Light (ID = 3)
* Unknown/No Light (ID = 4)

After the detection, the results are sent back to `tf_detection.py`, where it publishes to the `/traffic_waypoints` topic for the controller module to decelerate if needed.

### Example

Driving along the waypoints on the simulated highway:

![][image2]

Slowing down to a stop in front of the stop line for a red light:

![][image3]

---
## Try it yourself!
1. Clone the project repository
```bash
git clone https://github.com/udacity/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```
3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Port Forwarding
To set up port forwarding, please refer to the [instructions from term 2](https://classroom.udacity.com/nanodegrees/nd013/parts/40f38239-66b6-46ec-ae68-03afd8a601c8/modules/0949fca6-b379-42af-a919-ee50aa304e6a/lessons/f758c44c-5e40-4e01-93b5-1a82aa4e044f/concepts/16cf4a78-4fc7-49e1-8621-3450ca938b77)
