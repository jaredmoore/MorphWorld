class WorldObject():
    x = 0
    y = 0
    z = 0
    length = 1 #Size of x
    height = 1 #Size of y
    width = 1 #Size of z
    object_type = ""

    def __init__(self, x, y, z, length, height, width, type, opacity=1.0):
        """
            Creates a world_object

            Args: \n
                x - x location of the world_object. 
                y - y location of the world_object. 
                z - z location of the world_object.
                length - x size of the world_object.
                height - y size of the world_object.
                width - z size of the world_object.
                type - The world_object type for the visualizer.
                color - The color for the visualizer
                opacity - The opacity for the visualizer
        """
        self.x = x
        self.y = y
        self.z = z
        self.length = length
        self.height = height
        self.width = width
        self.object_type = type
        self.opacity = opacity

    def init_log(self, my_file):
        """
            Logs the setup information required for the object
        """
        temp = (self.object_type + ","
                    + str(self.x+(self.length/2)) + "," 
                    + str(self.y+(self.height/2)) + ","
                    + str(self.z+(self.width/2)) + "," 
                    + str(self.length) + ","
                    + str(self.height) + ","
                    + str(self.width) + ","
                    + "1,0,0,0\n")
        my_file.write(temp)

    def get_position_str(self):
        """
            Returns:
                The coordinates of the object in format for the visualizer
        """
        return str(self.x+(self.length/2)) + "," + str(self.y+(self.height/2)) + "," + str(self.z+(self.width/2))

    def get_rotation_str(self):
        """
            Returns:
                The rotaton of the object in format for the visualizer
        """
        return ("1,0,0,0")

    def set_opacity(self, num):
        """
            Sets the opacity of the object

            Args:
                num - The new opacity value
        """
        self.opacity = num

    def __repr__(self):
        return str(self.width) + 'x' + str(self.height) + ' - ' + str(self.opacity)

    def set_coords(self, coords):
            self.x = coords[0]
            self.y = coords[1]
            self.z = coords[2]