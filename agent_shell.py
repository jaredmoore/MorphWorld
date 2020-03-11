from world_object import WorldObject

class AgentShell(WorldObject):
    def __init__(self, x, y, z, length, height, width, opacity):
            WorldObject.__init__(self, x, y, z, length, height, width, "box", 0.0)

    def get_position_str(self):
        """
            Returns:
                The coordinates of the object in format for the visualizer
        """
        return str(self.x+(1/2)) + "," + str(self.y+(1/2)) + "," + str(self.z+(1/2))
    
    def init_log(self, my_file):
        """
            Logs the setup information required for the object
        """
        temp = (self.object_type + ","
                    + str(self.x+(1/2)) + "," 
                    + str(self.y+(1/2)) + ","
                    + str(self.z+(1/2)) + "," 
                    + str(self.length) + ","
                    + str(self.height) + ","
                    + str(self.width) + ","
                    + "1,0,0,0\n")
        my_file.write(temp)