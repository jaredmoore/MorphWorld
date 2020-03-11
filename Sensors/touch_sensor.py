from direction import Direction
from Sensors.base_sensor import BaseSensor
import math
import numpy
class TouchSensor(BaseSensor):
    def check_touch(self, world):
        """
            Returns:
                True if the sensor is touching something,
                False if the sensor is not.
        """
        return (Direction.calculate_coords(self.direction, 1, self.x, self.y, self.z) == 1)
        # shortest_distance = 1
        # #Right now is starting from coordnates 1
        # for i in range(1, self.view_distance+1): #Forward-Back
        #     for j in range(-1 * math.floor(self.view_height/2), math.floor(self.view_height/2) +1): #Up-Down
        #        for k in range(-1 * math.floor(self.view_width/2), math.floor(self.view_width/2) +1): #Left-Right
        #             coords = Direction.calculate_coords(self.direction, i, self.x, self.y, self.z)
        #             d = Direction.calculate_distance(self.direction, self.x, self.y, self.z, coords[0], coords[1], coords[2])
        #             if (not(coords[0] >= len(world.tunnel_world)) and not world.check_space(coords)):                             
        #                 temp = d/self.view_distance
        #                 if(temp < shortest_distance):
        #                     shortest_distance = temp             
        # return (1 if shortest_distance == 0 else 0)

    def get_indicator_color_str(self, world):
        """
            Returns:
                The color green if the sensor is not triggered. The color red if the snesor is triggered.
        """
        if self.check_touch(world):
            return "0xFF0000"
        else:
            return "0x00FF00"