from direction import Direction
import math
import numpy
class BaseSensor():
    """
        Initate sensor. 
        Args:\n
            view_distance - Specifys h  ow far the sensor can see
            x - x location of sensor
            y - y location of sensor
            z - z location of sensor
            view_width - Specifies how wide the cone of vision of it
            view_height - Specifies how height the cone of vision of it
            view_direction - Specifies the direction the cone is facing
    """
    SENSOR_DISPLACEMENT = .5 


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
        self.length = 0.3
        self.height = 0.3
        self.width = 0.3
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.direction = direction
        self.view_distance = view_distance
        self.view_width = view_width
        self.view_height = view_height
        self.relative_pos = Direction.calculate_normalized_coords(self.direction, tuple((self.x-agent.x, self.y-agent.y, self.z-agent.z)), tuple((agent.agent_length-1, agent.agent_height-1, agent.agent_width-1)))

    def set_pos_based_on_relative(self, agent):
        """
            Moves the sensor to the inputted coordinates.
            Args: \n
                x_dif - Change in x
                y_dif - Change in y
                z_dif - Change in z                       
        """
        if self.direction == Direction.NORTH or self.direction == Direction.SOUTH:
            if(self.relative_pos[0] > 0): 
                self.y = math.floor(agent.y + self.relative_pos[0]*agent.agent_height)
            else:
                self.y = math.ceil(agent.y + self.relative_pos[0]*agent.agent_height)

            if(self.relative_pos[1] > 0): 
                self.z = math.floor(agent.z + self.relative_pos[1]*agent.agent_width)
            else:
                self.z = math.ceil(agent.z + self.relative_pos[1]*agent.agent_width)
            
        elif self.direction == Direction.UP or self.direction == Direction.DOWN: 
            if(self.relative_pos[0] > 0): 
                self.x = math.floor(agent.x + self.relative_pos[0]*agent.agent_length)
            else:
                self.x = math.ceil(agent.x + self.relative_pos[0]*agent.agent_length)
            
            if(self.relative_pos[1] > 0): 
                self.z = math.floor(agent.z + self.relative_pos[1]*agent.agent_width)
            else:
                self.z = math.ceil(agent.z + self.relative_pos[1]*agent.agent_width)

        elif self.direction == Direction.WEST or self.direction == Direction.EAST:
            if(self.relative_pos[0] > 0): 
                self.y = math.floor(agent.y + self.relative_pos[0]*agent.agent_height)
            else:
                self.y = math.ceil(agent.y + self.relative_pos[0]*agent.agent_height)
            
            if(self.relative_pos[1] > 0): 
                self.x = math.floor(agent.x + self.relative_pos[1]*agent.agent_length)
            else:
                self.x = math.ceil(agent.x + self.relative_pos[1]*agent.agent_length)
        
    def move_sensor(self, x_dif, y_dif, z_dif):
        """
            Moves the sensor based on the inputted coordinates.
            Args: \n
                x_dif - Change in x
                y_dif - Change in y
                z_dif - Change in z                       
        """
        self.x += x_dif
        self.y += y_dif
        self.z += z_dif

        if(not float(self.x).is_integer() or not float(self.y).is_integer() or not float(self.z).is_integer()):
            raise ValueError("Sensor coordinate values MUST be integers")  
        else:
            self.x = int(self.x)
            self.y = int(self.y)
            self.z = int(self.z)
    
    def get_position_str(self):
        """
            Returns:
                The coordinates of the object in format for the visualizer
        """
        x = self.x+(1/2)
        y = self.y+(1/2)
        z = self.z+(1/2)
        if self.direction == Direction.NORTH:
            x += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.SOUTH:
            x -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.UP:
            y += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.DOWN:
            y -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.EAST:
            z -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.WEST:
            z += self.SENSOR_DISPLACEMENT

        return str(x) + "," + str(y) + "," + str(z)

    def get_rotation_str(self):
        """
            Returns:
                The rotaton of the object in format for the visualizer
        """
        return ("1,0,0,0")

    def init_log(self, my_file):
        """
            Logs the setup information required for the object
        """
        x = self.x+(1/2)
        y = self.y+(1/2)
        z = self.z+(1/2)
        if self.direction == Direction.NORTH:
            x += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.SOUTH:
            x -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.UP:
            y += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.DOWN:
            y -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.EAST:
            z -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.WEST:
            z += self.SENSOR_DISPLACEMENT

        temp = ("box,"
                    + str(x) + "," 
                    + str(y) + ","
                    + str(z) + "," 
                    + str(self.length) + ","
                    + str(self.width) + ","
                    + str(self.height) + ","
                    + "1,0,0,0\n")

        temp += ("box,"
                    + str(x+(self.view_distance/2)) + "," 
                    + str(y) + ","
                    + str(z) + "," 
                    + str(self.view_distance) + ","
                    + str(0.1) + ","
                    + str(0.1) + ","
                    + "1,0,0,0\n")
        my_file.write(temp)

    def get_indicator_position_str(self):
        x = self.x+(1/2)
        y = self.y+(1/2)
        z = self.z+(1/2)
        if self.direction == Direction.NORTH:
            x += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.SOUTH:
            x -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.UP:
            y += self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.DOWN:
            y -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.EAST:
            z -= self.SENSOR_DISPLACEMENT
        elif self.direction == Direction.WEST:
            z += self.SENSOR_DISPLACEMENT
        return (str(x+(self.view_distance/2)) + "," + str(y) + "," + str(z))

    def get_indicator_color_str(self, world):
        """
            Returns:
                The color green if the sensor is not triggered. The color red if the snesor is triggered.
        """
        return "0x000000"



