from Controllers.base_controller import BaseController
import random
from direction import Direction
class RandomController(BaseController):  

    def run(self):
        """
            Runs the random-based controller
        """
        total_frames = self.calculate_frames()
        for i in range(total_frames):
            #distance = self.check_distance_sensor(0)
            move = random.randint(0, 5) 
            if move == 0:
                self.move_direction(Direction.NORTH)
            if move == 1:
                self.move_direction(Direction.NORTH)
            if move == 2:
                self.move_direction(Direction.NORTH)
            if move == 3:
                self.move_direction(Direction.NORTH)
            if move == 4:
                self.move_direction(Direction.NORTH)
            if move == 5:
                self.move_direction(Direction.NORTH)
