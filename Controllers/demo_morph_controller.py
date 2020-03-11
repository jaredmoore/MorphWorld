from Controllers.base_controller import BaseController
import random
from direction import Direction
class DemoMorphController(BaseController):
    def run(self):
        self.move_direction(Direction.UP)
        # total_frames = self.calculate_frames()
        # thick = 1
        # for i in range(total_frames):
        #     for j in range(4):
        #         self.morph(thick)
        #     self.agent.x = 0
        #     self.agent.y = 5
        #     self.agent.z = 5
        #     thick *= -1