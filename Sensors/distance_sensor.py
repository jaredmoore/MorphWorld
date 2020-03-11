from Sensors.base_sensor import BaseSensor
from direction import Direction
import math
class DistanceSensor(BaseSensor):
    def __init__(self, agent, x, y, z, direction=Direction.NORTH, view_distance=5, view_width=1, view_height=1):
        """
            Initate sensor. 
            Args:\n
                
                agent - Used to calculate relative position
                x - x location of sensor
                y - y location of sensor
                z - z location of sensor
                direction - Specifies the direction the cone is facing
                view_distance - Specifys how far the sensor can see
                view_width - Specifies how wide the cone of vision of it
                view_height - Specifies how height the cone of vision of it
                
        """
        BaseSensor.__init__(self, agent, x, y, z, direction, view_distance, view_width, view_height)

    def check_distance(self, world):
        """
            Checks the if there is an object is within the vision cone. Does not return coordinates! 

            Args:\n
                world - The 3d list of the world.
            
            Returns:\n 
                Normalized distance to the closest object (0-1). 1 if there is no object in range.
        """
        if isinstance(self.x, float) or isinstance(self.y, float) or isinstance(self.z, float):
            print("Matt, you screwed up somewhere. Why is the sensor coordinates a float")
        shortest_distance = 1
        #Right now is starting from coordnates 1
        for i in range(1, self.view_distance+1): #Forward-Back
            for j in range(-1 * math.floor(self.view_height/2), math.floor(self.view_height/2) +1): #Up-Down
               for k in range(-1 * math.floor(self.view_width/2), math.floor(self.view_width/2) +1): #Left-Right
                    coords = Direction.calculate_coords(self.direction, i, self.x, self.y, self.z)
                    d = Direction.calculate_distance(self.direction, self.x, self.y, self.z, coords[0], coords[1], coords[2])
                    if (not(coords[0] >= len(world.tunnel_world)) and not world.check_space(coords)):                             
                        temp = d/self.view_distance
                        if(temp < shortest_distance):
                            shortest_distance = temp             
        return shortest_distance
    
    def get_indicator_color_str(self, world):
        """
            Returns:
                The color green if the sensor is not triggered. The color red if the sensor is triggered.
        """
        if self.check_distance(world) < 1:
            return "0xFF0000"
        else:
            return "0x00FF00"