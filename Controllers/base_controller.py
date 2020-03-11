from agent import Agent
from world import World
from direction import Direction
from Sensors.distance_sensor import DistanceSensor
from Sensors.touch_sensor import TouchSensor
import numpy, traceback, sys
class BaseController():
    """
        BaseController

        Args:\n
            world - world object
            agent - agent object
            seconds - seconds of the simulation
            frame_time - the time of each frame
    """
    def __init__(self, log_file, world, agent, seconds, frame_time):
        """
            BaseController

            Args:\n
                world - world object
                agent - agent object
                seconds - seconds of the simulationy
                frame_time - the time of each frame
        """
        self.world = world
        self.agent = agent
        self.seconds = seconds
        self.frame_time = frame_time
        self.log_file = log_file
        self.csv_file = "Log Files/Sensor Data: " + log_file[10:-4] + ".csv"
        self.steps_taken = -1
        self.log()
        


    def move_direction(self, direction):
        """
            Commits the move given on the move list based on the direction.
            The update function that moves the agent in the world if possible.
            In essence, each update represents a frame in the simulation
                NORTH(1) - moves[0]
                SOUTH(-1) - moves[1]
                UP(2) - moves[2]
                DOWN(-2) = moves[3]
                WEST(3) = moves[4]
                EAST(-3) = moves[5]  
        """
        self.agent.generate_moves(self.world)
        self.agent.set_coords(self.agent.moves[abs(direction.value)])
        self.log()


    def change_velocity(self, velocity):
        """
            Changes the velocity of the agent

            Args:\n
                velocity - New velocity of the agent
        """
        self.agent.velocity = velocity


    def morph(self, thickness):
        """
            Morphs the agent given the thickness

            Arg:
                thickness - Positive value to increase the width/decrease the height, 
                            Negative value to decrease the width/increase the height.
        """
        result = self.agent.morph(thickness, self.world)
        self.log()
        return result


    def calculate_frames(self):
        """
            Returns the integer value of the amount of frames in the simulation
        """
        return int(self.seconds/self.frame_time)


    def get_sensor_count(self):
        """
            Returns the amount of sensors in the agent
        """
        return len(self.agent.sensors)


    def check_distance_sensor(self, num):
        """
            Returns the distance sensor output of the given sensor
        """
        return self.agent.sensors[num].check_distance(self.world)

    def check_all_distance_sensors(self):
        """
            Returns the distance sensor output of the given sensor
        """
        result = []
        for sensor in self.agent.sensors:
            if isinstance(sensor, DistanceSensor):
                result.append(sensor.check_distance(self.world))
            else:
                result.append(None)
        return result

    def check_percent_distance_sensors(self):
        """
            Gets the amount of activated distance sensors.

            Returns:
                A percentage of activated sensors
            
        """
        activated = 0
        sensors = 0
        for sensor in self.agent.sensors:
            if isinstance(sensor, DistanceSensor):
                if(sensor.check_distance(self.world) < 1):
                    activated += 1
                sensors += 1
        return activated/sensors

    def check_touch_sensor(self, num):
        """
            Returns the touch sensor output of the given sensor
        """
        return self.agent.sensors[num].check_touch(self.world)
    
    def check_all_touch_sensors(self):
        """
            Returns the distance sensor output of the given sensor
        """
        result = []
        for sensor in self.agent.senssors:
            if isinstance(sensor, TouchSensor):
                result.append(sensor.check_touch(self.world))
            else:
                result.append(None)
        return result

    def at_end(self):
        """
            Check's whether or not the agent has won or not. 

            Return:
                True - If the agent is at the end of the tunnel
                False - If the agent is not at the end of the tunnel
        """
        return (self.agent.x == len(self.world.tunnel_world)-1)

    def run(self):
        """
            Runs the base controller. Override this method..
        """
        #Amount of frames should be seconds/frame_times
        total_frames = self.calculate_frames()
        for i in range(total_frames):
            distance = self.check_distance_sensor(0)
            touch = self.check_touch_sensor(0)
            print("Distance: " + str(distance))
            print("Touch: " + str(touch))
            self.move_direction(Direction.NORTH)

    def log(self):
        """
            Logs the state of the world based for the following: 
            - Agent location/rotation
            - Obstacle location/rotation
            
            Args:
                agent - the agent that needs to be loged
        """
        my_file = open(self.log_file, "a")
        

        """
            Position Logging
        """
        object_positions = []

        #Agent
        object_positions.append(self.agent.camera.get_position_str())
        for i in self.agent.morphs:
            object_positions.append(i.get_position_str())

        #Sensor and Sensor indicators
        for sensor in self.agent.sensors:
            object_positions.append(sensor.get_position_str())
            object_positions.append(sensor.get_indicator_position_str())

        #Obstacles
        for obstacle in self.world.world_objects:
            object_positions.append(obstacle.get_position_str())

        my_file.write(",".join(object_positions) + "\n")
        
        """
            Rotation Logging
        """
        object_rotations = []

        #Agent
        for i in range(len(self.agent.morphs)+1):
            object_rotations.append(self.agent.get_rotation_str())

        #Sensors and Sensor indicators
        for sensor in self.agent.sensors:
            object_rotations.append(sensor.get_rotation_str())
            object_rotations.append(sensor.get_rotation_str())

        #Obstacle
        for x in self.world.world_objects:
            object_rotations.append(x.get_rotation_str())

        my_file.write(",".join(object_rotations) + "\n")

        """
            Color Logging
        """
        object_colors= []

        #Agent
        object_colors.append("0xFFFFFF")
        for i in range(len(self.agent.morphs)):
            object_colors.append("0x0063ba")

        #Sensors and Sensor indicators
        for sensor in self.agent.sensors:
            object_colors.append("0xFFFFFF")
            object_colors.append(sensor.get_indicator_color_str(self.world))

        #Obstacle
        for x in self.world.world_objects:
            object_colors.append("0x222222")

        my_file.write(",".join(object_colors) + "\n")

        """
            Opacity Logging
        """
        object_opacity = []

        #Agent
        object_opacity.append("0.0")
        object_opacity.extend(self.agent.get_morph_opacities())
        
        #Sensors and Sensor indicators
        for sensor in self.agent.sensors:
            object_opacity.append("1.0")
            object_opacity.append("0.8")

        #Obstacle
        for x in self.world.world_objects:
            object_opacity.append("1.0")

        my_file.write(",".join(object_opacity) + "\n")
            
        my_file.close()

        csv_file = open(self.csv_file, "a")
        sensor_values = []

        if not self.at_end():
            self.steps_taken += 1
