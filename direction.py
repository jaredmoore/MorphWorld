from enum import Enum
import math, numpy
class Direction(Enum):
    """
        NORTH - X Positive | 1 - moves[0]\n
        SOUTH - X Negative |-1 - moves[1]\n
        UP    - Y Positive | 2 - moves[2]\n
        DOWN  - Y Negative |-2 - moves[3]\n
        EAST  - Z Negative | 3 - moves[4]\n
        WEST  - Z Positive |-3 - moves[5]\n
    """
    NORTH = 0 #X Positive 0
    SOUTH = -1 #X Negative 1
    UP = 2 #Y Positive 2
    DOWN = -3 #Y Negative 3
    WEST = 4 #Z Positve 4
    EAST = -5 #Z Negative 5  

    @staticmethod
    def calculate_distance(direction, x1, y1, z1, x2, y2, z2):
        """
            Calculates the distance between to points in 3D plane

            Args:\n
                x1 - The x of the first point
                y1 - The y of the first point
                z1 - The z of the first point
                x2 - The x of the second point
                y2 - The y of the second point
                z2 - The z of the second point

            Returns:\n
                The calculated distance 
        """
        if direction == Direction.NORTH:
            x1 += 1
        elif direction == Direction.WEST:
            z1 += 1
        elif direction == Direction.SOUTH:
            x1 -= 1
        elif direction == Direction.EAST:
            z1 -= 1
        elif direction == Direction.UP:
            y1 += 1
        elif direction == Direction.DOWN:
            y1 -= 1

        distance = math.sqrt(math.pow(x2 - x1, 2) + math.pow(y2 - y1, 2) + math.pow(z2 - z1, 2) * 1.0)
        return distance
    
    @staticmethod
    def calculate_coords(direction, distance, x, y, z):
        """
            Calculates the coordinates given the distance, direction and position\n

            Args:\n
                direction - The direction to calculate towards\n
                distance - The distance to calcuate\n
                x - x position of the source\n
                y - y position of the source\n
                z - z position of the source\n
        """
        # if direction == Direction.NORTH: 
        #     x = math.ceil(x)
        # elif direction == Direction.SOUTH:
        #     x = math.floor(x)
        # elif direction == Direction.UP: 
        #     y = math.ceil(y)
        # elif direction == Direction.DOWN:
        #     y = math.floor(y)
        # elif direction == Direction.WEST:
        #     z = math.ceil(z)
        # elif direction == Direction.EAST:
        #     z = math.floor(z)

        if direction == Direction.NORTH:
            return tuple((x+distance, y, z))
        elif direction == Direction.SOUTH:
            return tuple((x-distance, y, z))
        elif direction == Direction.UP:
            return tuple((x, y+distance, z))
        elif direction == Direction.DOWN:
            return tuple((x, y-distance, z))
        elif direction == Direction.EAST:
            return tuple((x, y, z-distance))
        elif direction == Direction.WEST:
            return tuple((x, y, z+distance))

    @staticmethod
    def calculate_dimensions_by_direction(direction, x_size, y_size, z_size):
        """
            Gets the "height" and "width" based on the direction faced

            Args:
                direction - Given direction
                x_size - x size
                y_size - y size
                z_size - z size

            Returns:
                tuple of height and width
        """
        if direction == Direction.NORTH or direction == Direction.SOUTH: 
            length = x_size
            height = y_size
            width = z_size
        elif direction == Direction.UP or direction == Direction.DOWN: 
            length = y_size
            height = x_size
            width = z_size
        elif direction == Direction.WEST or direction == Direction.EAST:
            length = z_size
            height = y_size
            width = x_size

        return tuple((length, height, width))

    @staticmethod
    def calculate_normalized_coords(direction, coords, dimensions):
        """
            Gets the relative "height" and relative "width" based on the direction faced

            Args:
                direction - Given direction
                coords - Tuple that holds x, y, z
                dimensions - Tuple that holds length, width, and height

            Returns:
                tuple of relative height and relative width
        """
        if direction == Direction.NORTH or direction == Direction.SOUTH: 
            relative_height = coords[1]/dimensions[1]
            relative_width = coords[2]/dimensions[2]
        elif direction == Direction.UP or direction == Direction.DOWN: 
            relative_height = coords[0]/dimensions[0]
            relative_width = coords[2]/dimensions[2]
        elif direction == Direction.WEST or direction == Direction.EAST:
            relative_height = coords[1]/dimensions[1]
            relative_width = coords[0]/dimensions[0]
        return tuple((relative_height, relative_width))
        

    @staticmethod
    def calculate_range(direction, distance, x, y, z, height, width):
        """
            Calculates the range of coordinates\n

            Args:\n
                direction - The direction to calculate towards\n
                distance - The distance to calcuate\n
                x - x position of the source\n
                y - y position of the source\n
                z - z position of the source\n
                height - Height in which to calculate\n
                width - Height in which to calculate\n
                start_distance = 0 - Distance in which to start calculating at
            
            Returns:\n
                tuples of coords tuples, giving the range of coordinates
        """
        
        facing = numpy.sign(direction.value)
        if facing == 0:
            facing = 1

        #Forward
        i = distance * facing

        #Up-Down
        j1 = -1 * math.floor(height/2)
        j2 = math.floor(height/2)

        #Left-Right
        k1 = -1 * math.floor(width/2)
        k2 = math.floor(width/2)     

        #Facing X plane
        if direction == Direction.NORTH or direction == Direction.SOUTH: 
            #x: Forward-Back (i)
            x1 = x
            x2 = x + i 

            #y: Up-Down (j)
            y1 = math.ceil(y + j1) 
            y2 = math.floor(y + j2)

            #z: Left-right (k)
            z1 = math.ceil(z + k1)
            z2 = math.floor(z + k2) 

        #Facing Y plane
        elif direction == Direction.UP or direction == Direction.DOWN:
            #x: Up-Down (j)
            x1 = math.ceil(x + j1) 
            x2 = math.floor(x + j2)

            #y: Forward-Back (i)
            y1 = y
            y2 = y + i 

            #z: Left-right (k)
            z1 = math.ceil(z + k1)
            z2 = math.floor(z + k2)
        
        #Facing Z plane
        elif direction == Direction.WEST or direction == Direction.EAST:
            #x: Left-right (k)
            x1 = math.ceil(x + k1) 
            x2 = math.floor(x + k2)

            #y: Up-Down (j)
            y1 = math.ceil(y + j1)
            y2 = math.floor(y + j2) 

            #z: Forward-Back (i)     
            z1 = z
            z2 = z + i 

        coord1 = tuple((x1, y1, z1))
        coord2 = tuple((x2, y2, z2))

        return tuple((coord1, coord2))
   
