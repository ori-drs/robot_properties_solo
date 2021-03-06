""" Basic loading of the Solo robot with the srdf file. Example of collision checking and display with gepetto-gui. """

import pinocchio as pin
import numpy as np
import rospkg
import time
import os
from os.path import join

from robot_properties_solo.config import Solo12Config

if __name__ == "__main__":
    #  Load the robot urdf.
    robot = Solo12Config.buildRobotWrapper()

    #  Setup the display (connection to gepetto viewer) and load the robot model.
    robot.initDisplay(loadModel=True)

    #  Add collision pairs
    robot.collision_model.addAllCollisionPairs()

    #  Find the absolute path to the srdf file
    srdf_path = (
        join(rospkg.RosPack().get_path("robot_properties_solo"),
             "srdf",
             "solo.srdf")
    )
    
    #  Disable collision pairs specified in the srdf
    pin.removeCollisionPairs(robot.model, robot.collision_model, srdf_path)

    #  Read the reference configurations defined in the srdf
    pin.loadReferenceConfigurations(robot.model, srdf_path)
    q = robot.model.referenceConfigurations["straight_standing"]

    #  Display the configuration in the viewer.
    robot.display(q)

    #  Initialize the collision data
    robot.collision_data = pin.GeometryData(robot.collision_model)

    #  Compute all the collisions
    pin.computeCollisions(robot.model, robot.data, robot.collision_model,
 robot.collision_data, q, False)

    #  Print the status of collision for all collision pairs
    valid = True
    for k in range(len(robot.collision_model.collisionPairs)): 
        cr = robot.collision_data.collisionResults[k]
        cp = robot.collision_model.collisionPairs[k]
        #print("collision pair:",cp.first,",",cp.second,"- collision:","Yes" if cr.isCollision() else "No") #  Optionnal display of all the collision pairs
        if cr.isCollision():
            valid = False
    print("## First configuration valid: ", valid) 
    
    #  Move to a configuration in self collision
    q[9] = 1
    q[15] = -2
    robot.display(q)

    #  Compute all the collisions
    pin.computeCollisions(robot.model, robot.data, robot.collision_model,
 robot.collision_data, q, False)

    #  Print the status of collision for all collision pairs
    valid = True
    for k in range(len(robot.collision_model.collisionPairs)): 
        cr = robot.collision_data.collisionResults[k]
        cp = robot.collision_model.collisionPairs[k]
        #print("collision pair:",cp.first,",",cp.second,"- collision:","Yes" if cr.isCollision() else "No") #  Optionnal display of all the collision pairs
        if cr.isCollision():
            valid = False
    print("## Second configuration valid: ", valid) 


  
