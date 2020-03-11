from world_object import WorldObject
from direction import Direction
from agent_shell import AgentShell
from Sensors.distance_sensor import DistanceSensor
import warnings, numpy, math

class Agent():
    """
        Creates an agent

        Args:\n
            x - x location of the object
            y - y location of the object
            z - z location of the object
            length - x size of the object
            height - y size of the object
            width - z size of the object
            velocity - The speed of the object
    """ 


    #Sensor: Dist, touch, velocity
    def __init__(self, x, y, z, size=1, velocity=1):
        """
            Creates an agent

            Args:\n
                    x - x location of the object
                    y - y location of the object
                    z - z location of the object
                    size - size of the robot (Volume in Blocks)
                    velocity - The speed of the object
        """
        self.x = x
        self.y = y
        self.z = z

        if (size % 2 == 0): 
            #Shift lower when possible; otherwise, shift higher 
            if (self.y - size/2 >= 0):
                self.y -= 0.5    
            else:
                self.y += 0.5
            if (self.z - size/2 >= 0):
                self.z -= 0.5    
            else:
                self.z += 0.5
            print("WARNING: Even shaped agents cannot have integer value coordinates. Automatically shifted to: ", self.x, self.y, self.z)


        self.agent_length = 1
        self.agent_width = size
        self.agent_height = size
        self.init_volume = size*size
        self.velocity = velocity
        self.moves = [] #A list of possible moves
        self.sensors = []
        
        #Agent Visualization
        self.camera = WorldObject(x, y, z, 0, 0, 0, "box", 0.0)
        self.morphs = []
        
        self.generate_morphs()

    def generate_preset_sensors(self):
        """
            Generates sensors in the corners and the center
        """
        self.append_sensor(DistanceSensor(self, self.x, math.ceil(self.y-self.agent_height/2), math.ceil(self.z-self.agent_width/2)))
        self.append_sensor(DistanceSensor(self, self.x, math.ceil(self.y-self.agent_height/2), math.floor(self.z+self.agent_width/2)))
        self.append_sensor(DistanceSensor(self, self.x, math.floor(self.y), math.floor(self.z)))
        self.append_sensor(DistanceSensor(self, self.x, math.floor(self.y+self.agent_height/2), math.ceil(self.z-self.agent_width/2)))
        self.append_sensor(DistanceSensor(self, self.x, math.floor(self.y+self.agent_height/2), math.floor(self.z+self.agent_width/2)))


    def get_coords(self):
        """
            Returns the current coordinates of the agent.

            Returns:\n
                A tuple of (x, y, z)
        """
        temp = tuple((self.x, self.y, self.z))
        return temp

    def get_morph_opacities(self):
        opacities = []
        for i in self.morphs:
            opacities.append(str(i.opacity))
        return opacities

    def get_rotation_str(self):
        """
            Returns:
                The rotaton of the object in format for the visualizer
        """
        return ("1,0,0,0")


    def set_coords(self, coords):
        """
            Sets the coordinates of the agent.\n

            Args:\n
                coords - A tuple of (x, y, z)

            Throws:\n
                ValueError - If the move given is not in the move list
        """
        if coords not in self.moves:
            raise ValueError("The move given is not possible for the agent")
        else:
            #Calculate differences for sensors
            x_dif = coords[0] - self.x
            y_dif = coords[1] - self.y
            z_dif = coords[2] - self.z

            if(not float(x_dif).is_integer() or not float(y_dif).is_integer() or not float(z_dif).is_integer()):
                raise ValueError("The different in coordinates for the agent MUST be integers. Don't know how we got here in the first place...")  
            else:
                x_dif = int(x_dif)
                y_dif = int(y_dif)
                z_dif = int(z_dif)
            
            #Move the agent
            self.x = coords[0]
            self.y = coords[1]
            self.z = coords[2]

            #Move the camera
            self.camera.set_coords(coords)

            #Move the shell
            self.morphs[self.morph_index].set_coords(coords)

            for sensor in self.sensors:
                sensor.move_sensor(x_dif, y_dif, z_dif)

    def append_sensor(self, sensor):
        self.sensors.append(sensor)
        

    def morph(self, thickness, world):
        """
            Changes the thickness of the agent.
            Args:
                thickness - Positive value to increase the width/decrease the height, 
                            Negative value to decrease the width/increase the height.
            Returns:
                True - When morph is successful
                False - When morph is unsuccessful

        """
        print('Coordinates Before Morph: ', self.x, self.y, self.z)

        # Validation for thickness/thiness
        if thickness == 1:
            if self.agent_height == 1:
                print("WARNING: Cannot thicken any further. Agent thickness is maxed out.")
                return False
        elif thickness == -1:
            if self.agent_width == 1:
                print("WARNING: Cannot thin down any further. Agent thickness is already at a minimum.")
                return False            


        # Handling new Y and height
        new_y = self.y
        new_height = self.morphs[self.morph_index+thickness].height

        # From an even height to an odd height
        if (new_height % 2 == 0 and self.agent_height % 2 == 1): 
            #Shift lower when possible; otherwise, shift higher 
            if (self.y - new_height/2 >= 0):
                new_y -= 0.5    
            else:
                new_y += 0.5
        
        # From an odd height to an even height
        if (new_height % 2 == 1 and self.agent_height % 2 == 0): 
            #Shift "back" higher when possible; otherwise, shift lower
            if (self.y + new_height/2 >= len(world.tunnel_world[0])):
                new_y += 0.5
            else:
                new_y -= 0.5


        # Handling new Z and width
        new_z = self.z
        new_width = self.morphs[self.morph_index+thickness].width
        
        # From an even width to an odd width
        if (new_width % 2 == 0 and self.agent_width % 2 == 1): 
            #Shift to the right when possible; otherwise, shift to the left
            if (self.z - new_width/2 >= 0):
                new_z -= 0.5    
            else:
                new_z += 0.5
        
        # From an odd width to an even width
        if (new_width % 2 == 1 and self.agent_width % 2 == 0): 
            #Shift "back" to the left when possible; otherwise, shift right
            if (self.z + new_width/2 >= len(world.tunnel_world[0][0])):
                new_z += 0.5
            else:
                new_z -= 0.5


        # Checks to see if this new morph is possible            
        coords = tuple((tuple((self.x, math.ceil(new_y-new_height/2), math.ceil(new_z-new_width/2))), tuple((self.x, math.floor(new_y+new_height/2), math.floor(new_z+new_width/2)))))
        if(not world.check_spaces(coords[0], coords[1])):
            print("WARNING: Morph is impossible, would cause a collision into a wall.")
            return False

        #Calculates the new location of sensors
        #Removes current morph from the scene
        self.morphs[self.morph_index].set_opacity(0.0)
        self.morphs[self.morph_index].x = 1000
        self.morphs[self.morph_index].y = 1000
        self.morphs[self.morph_index].z = 1000

        #Goes to the next morph
        self.morph_index += thickness

        #Move the agent
        self.x = self.x
        self.y = new_y
        self.z = new_z

        #Move the camera
        self.camera.set_coords(self.get_coords())

        self.morphs[self.morph_index].set_opacity(1.0)
        self.morphs[self.morph_index].x = self.x            
        self.morphs[self.morph_index].y = self.y
        self.morphs[self.morph_index].z = self.z

        #Sets the agents width/height to the current morph
        self.agent_height = self.morphs[self.morph_index].height
        self.agent_width = self.morphs[self.morph_index].width 

        #Move the sensors
        for sensor in self.sensors:
            sensor.set_pos_based_on_relative(self)
        print(self.morphs)
        print('Coordinates After Morph: ', self.x, self.y, self.z)
        print('=====================================')
        return True

    def generate_moves(self, world):
        """
            Generates all the possible moves of the agent.
            
            Args:\n
                world - A 3d list representing the world
        """
        self.moves = []

        #init_coords = tuple((self.x, self.y, self.z))

        # Goes through each direction
        for direction in Direction:      

            # We can add everything to the list because we are just checking to see if that move is possible
            if direction == Direction.NORTH: 
                current = math.ceil(self.x)
            elif direction == Direction.SOUTH:
                current = math.floor(self.x)
            elif direction == Direction.UP: 
                current = math.ceil(self.y)
            elif direction == Direction.DOWN:
                current = math.floor(self.y)
            elif direction == Direction.WEST:
                current = math.ceil(self.z)
            elif direction == Direction.EAST:
                current = math.floor(self.z)
            
            # Future at the end of this block will contain the furtherest possible move
            future = tuple((self.x, self.y, self.z))

            # Facing determines if we are going in a positive or negative direction
            facing = numpy.sign(direction.value)
            if facing == 0:
                facing = 1

            # Dim hold the (length, height, width) relative to the direction that it is facing
            dim = Direction.calculate_dimensions_by_direction(direction, self.agent_length, self.agent_height, self.agent_width) 
            
            # This for loop checks v (velocity-value) spaces ahead. Checks the path forward by one unit in each iteration. Accounts for morphology
            for dis in range(current, current+facing*self.velocity, facing): 
                # Coords holds the range of coords, that represents the path of the block. Vital for accounting for its morphology
                #BUG: Problem is here. The calculation doesn't account for "left/right/up/down" "length" when looking that direction
                if direction == Direction.NORTH: #Positive X
                    temp = math.floor(future[0] + dim[0]/2)
                    temp_coords = tuple((temp, future[1], future[2]))
                elif direction == Direction.SOUTH: #Negative X
                    temp = math.ceil(future[0] - dim[0]/2)
                    temp_coords = tuple((temp, future[1], future[2]))
                elif direction == Direction.UP: #Positive Y
                    temp = math.floor(future[1] + dim[0]/2)
                    temp_coords = tuple((future[0], temp, future[2]))
                elif direction == Direction.DOWN: #Negative Y
                    temp = math.ceil(future[1] - dim[0]/2)
                    temp_coords = tuple((future[0], temp, future[2]))
                elif direction == Direction.WEST: #Positive Z
                    temp = math.floor(future[2] + dim[0]/2)
                    temp_coords = tuple((future[0], future[1], temp))
                elif direction == Direction.EAST: #Negative XZ
                    temp = math.ceil(future[2] - dim[0]/2)
                    temp_coords = tuple((future[0], future[1], temp))

                coords = Direction.calculate_range(direction, 1, temp_coords[0], temp_coords[1], temp_coords[2], dim[1], dim[2])
                
                # Checks to see if the path is possible. Re-sets the future coords if possible
                if(world.check_spaces(coords[0], coords[1])):
                    future = Direction.calculate_coords(direction, 1, future[0], future[1], future[2])
                else:
                    break
            # Append the latest possible move of the direciton
            self.moves.append(future)

    def generate_morphs(self):
        """
            Generates a list of all the possible morphs
        """
        list_size = 2*(math.sqrt(self.init_volume)) - 1
        self.morph_index = int(list_size/2)

        x = 1
        y = self.init_volume
        
        for i in range(0, self.morph_index):
            self.morphs.append(AgentShell(1000, 1000, 1000, 1, x, y, 0.0))
            x += 1
            y = self.justify_morph(y, x, True)
        for i in range(0, self.morph_index):
            self.morphs.append(AgentShell(1000, 1000, 1000, 1, x, y, 0.0))
            y -= 1
            x = self.justify_morph(x, y)
        self.morphs.append(AgentShell(1000, 1000, 1000, 1, x, y, 0.0))

        #Puts the current morph into the scene
        self.morphs[self.morph_index].set_opacity(1.0)
        self.morphs[self.morph_index].x = self.x     
        self.morphs[self.morph_index].y = self.y
        self.morphs[self.morph_index].z = self.z
        self.morphs.reverse()

        print(self.morphs)

    def justify_morph(self, x1, x2, sub=False):
        """
            Helper method for morph. Helps determine how much extra width or height needs to be added.

            Args:
                x1 - The dimension that we are changing
                x2 - The dimension that has already changed

            Returns:
                The new x1 term.             
        """

        if x1 == 1 and x2 == 1:
            return x1

        new_size = x1 * x2
        n_x1 = x1
        if not sub:
            while(new_size < self.init_volume):
                n_x1 += 1
                new_size = x2 * n_x1
        else:
            while(new_size >= self.init_volume):
                prev_x1 = n_x1
                n_x1 -= 1
                new_size = x2 * n_x1
            n_x1 = prev_x1
        return n_x1