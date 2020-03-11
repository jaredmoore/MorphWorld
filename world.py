import os 
import random 
import numpy
import warnings
import math
from agent import Agent
from direction import Direction
from world_object import WorldObject


class World():
    """
        The constructor creates the tunnel world and sets up the logging file. 

        Args:
            frame_time - The amount of time in seconds one frame takes in the simulation | 
            seconds - The amount of time the simulation will take | 
            agent - A agent object describing the agent in the world | 
            world_length - The given length of the world (x) | 
            world_height - The given height of the world (y) | 
            world_with - The given width of the world (z) | 
            obstacles - The amount of obstacles to generate in the world. 
    """ 

    def __init__(self, log_file, frame_time, seconds, 
                    agent, world_length, world_height, 
                    world_width, obstacles):
        """
            The constructor creates the tunnel world and sets up the logging file. 

            Args:
                frame_time - The amount of time in seconds one frame takes in the simulation | 
                seconds - The amount of time the simulation will take | 
                agent - A agent object describing the agent in the world | 
                world_length - The given length of the world (x) | 
                world_height - The given height of the world (y) | 
                world_with - The given width of the world (z) | 
                obstacles - The amount of obstacles to generate in the world. 
        """
        self.world_objects = []
        self.gap_coords = []
        if obstacles > world_length/4:
            obstacles = math.floor(world_length/4)-1
            print(str(obstacles))
            warnings.warn("Too many obstacles requested, defaulting to max safe number: " + str(obstacles))

        #Set up logging file
        print("Initializing setup file...")


        setup_info = ("Version 0.4\n<setup information>\n" 
                    + str(seconds) + "\n" 
                    + str(frame_time) + "\n")
                    
        my_file = open(log_file, "a")
        my_file.write(setup_info)
        
        #Work with the world
        print("Generating World...")
        self.tunnel_world = [[ [0 for k in range(world_width)] for j in range(world_height)] for i in range(world_length)] 
        
        #Init Logging

        #Agent
        agent.camera.init_log(my_file)
        for i in agent.morphs:
            i.init_log(my_file)

        #Sensors
        for sensor in agent.sensors:
            sensor.init_log(my_file)

        #Length between obstacles
        obstacle_length = round(world_length/(obstacles))
        print("Generating Obstacles...")
        for o in range(0, obstacles):
            self.generate_obstacle(o*obstacle_length+2, my_file)

        my_file.write("<\setup information>\n<color information>\n")     

        #Colors
        object_colors= []

        #Agent
        object_colors.append("0xFFFFFF")
        for i in range(len(agent.morphs)):
            object_colors.append("0x0063ba") #Grand Valley's color

        #Sensors
        for sensor in agent.sensors:
            object_colors.append("0xFFFFFF")
            object_colors.append("0x00FF00")

        #Obstacle
        for x in self.world_objects:
            object_colors.append("0x222222")

        my_file.write(",".join(object_colors) + "\n<\color information>\n")  
        my_file.close()


        print("Initalization Complete!")

    def record_obstacle(self, x, y, z, 
                    length, height, width):
        """
            Fills in the range given in tunnel_world with 1s\n

            Args:\n
                x - x location of the object\n
                y - y location of the object\n
                z - z location of the object\n
                length - x size of the object\n
                height - y size of the object\n
                width - z size of the object\n
        """
        for i in range(x, x+length):
            for j in range(y, y+height):
                for k in range(z, z+width):
                    self.tunnel_world[i][j][k] = 1

    def generate_obstacle(self, x_pos, my_file):
        """
            Generates an random obstaclce at the given x position

            Args:
                x_pos - The x location to generate the obstacle | 
                my_file - A file object of the logged file
        """
        world_height = len(self.tunnel_world[0])
        world_width = len(self.tunnel_world[0][0])
        ##print("Generating Obstacle: \nx_pos: " + str(x_pos) 
        ##        + "| world_height: " + str(world_height)
        ##       + "| world_width: " + str(world_width))
        # 0 - y fill (Vertical Gap), 1 - y fill (Horizontal Gap)
        fill_orientation = random.randint(0, 1) 

        ##print("fill_orientation: " + str(fill_orientation))

        gap_length = random.randint(1, 4)
        ##print("Gap length: " + str(gap_length))
        #Generate Gap_size
        gap_size = round(numpy.random.normal(3, 1))
        if gap_size <= 0:
            gap_size = 1
        elif gap_size >= 6:
            gap_size = 5 
        ##print("Gap Size: " + str(gap_size))

        #Fill by y difference(Vertical Gap)
        if fill_orientation == 0: 
            #Generate Gap location
            gap_location = random.randint(0, world_height-gap_size)
            ##print("Gap Location: " + str(gap_location))
        
            #Box 1
            self.record_obstacle(x_pos, 0, 0, gap_length, gap_location, world_width) #Fill ins location on matrix
            box_1 = WorldObject(x_pos, 0, 0, gap_length, gap_location, world_width, "box") #Create Object
            box_1.init_log(my_file) #Log this in setup
            self.world_objects.append(box_1) #Add the object to the list

            #Box 2
            self.record_obstacle(x_pos, gap_location+gap_size, 0, gap_length, world_height-gap_location-gap_size, world_width) #Fill in the matrix locations            
            box_2 = WorldObject(x_pos, gap_location+gap_size, 0, gap_length, world_height-gap_location-gap_size, world_width, "box") #Create Object
            box_2.init_log(my_file) #Log this in setup
            self.world_objects.append(box_2) #Add the object to the list

            self.gap_coords.append(tuple((x_pos, gap_location+(gap_size/2), len(self.tunnel_world[0][0])/2)))
           
        #Fill by z difference (Horizontal Gap)
        elif fill_orientation == 1: 
            ##print("Horizontal Gap")

            #Generate Gap location
            gap_location = random.randint(0, world_width-gap_size) # 1 to width-2
            ##print("Gap Location: " + str(gap_location))

            #Box 1            
            self.record_obstacle(x_pos, 0, 0, gap_length, world_height, gap_location) #Fill in matrix locations
            box_1 = WorldObject(x_pos, 0, 0, gap_length, world_height, gap_location, "box") #Create Object
            box_1.init_log(my_file) #Log this in setup
            self.world_objects.append(box_1) #Add the object to the list

            #Box 2
            self.record_obstacle(x_pos, 0, gap_location+gap_size, gap_length, world_height, world_width-gap_location-gap_size) #Fill in matrix locations
            box_2 = WorldObject(x_pos, 0, gap_location+gap_size, gap_length, world_height, world_width-gap_location-gap_size, "box") #Create Object
            box_2.init_log(my_file) #Log this in setup
            self.world_objects.append(box_2) #Add the object to the list

            self.gap_coords.append(tuple((x_pos, len(self.tunnel_world[0])/2, gap_location+(gap_size/2))))
    
    def check_space(self, coords):
        """
            Args:
                coords - Tuple of the coordinates
            Returns:
                True - If the agent can reach the given coordinates
                False - If the agent cannot reach the given coordinates
        """
        if isinstance(coords[0], float) or isinstance(coords[1], float) or isinstance(coords[2], float):
            raise ValueError("These coordinates shouldn't be floats...")
        x = coords[0]
        y = coords[1]
        z = coords[2]
        
        x_bound = len(self.tunnel_world)
        y_bound = len(self.tunnel_world[0])
        z_bound = len(self.tunnel_world[0][0])
        return (x >= 0 and x < x_bound and 
                y >= 0 and y < y_bound and 
                z >= 0 and z < z_bound and
                self.tunnel_world[x][y][z] == 0)

    def check_spaces(self, coords1, coords2):
        """
            Args:
                coords - Tuple of the range of coordinates
            Returns:
                True - If the agent can reach the range of given coordinates
                False - If the agent cannot reach the range of given coordinate
        """
        for i,j in zip(coords1, coords2):
            if isinstance(i, float) or isinstance(j, float):
                raise ValueError("The coordinates given in World.check_spaces() are floats...")
        x_change = 1 if coords1[0] <= coords2[0] else -1
        y_change = 1 if coords1[1] <= coords2[1] else -1
        z_change = 1 if coords1[2] <= coords2[2] else -1

        for x in range(coords1[0], coords2[0]+x_change, x_change): 
            for y in range(coords1[1], coords2[1]+y_change, y_change):
                for z in range(coords1[2], coords2[2]+z_change, z_change):
                    temp = tuple((x, y, z))
                    if not self.check_space(temp):
                        return False
        return True