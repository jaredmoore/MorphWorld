from Controllers.base_controller import BaseController
from direction import Direction
import random
class RuleBasedController(BaseController):  
    def move_side(self):
        """
            Randomly move up/down or left/right
        """
        if self.attempts >= self.attempt_threshold:
            self.new_direction = True
            self.attempts = 0

        if self.new_direction is True:
            move = self.last_move
            while(move == self.last_move):          
                move = random.randint(0, 3) 
            if move == 0:
                self.last_move = 0
                self.move_direction(Direction.UP)
            elif move == 1:
                self.last_move = 1
                self.move_direction(Direction.DOWN)
            elif move == 2:
                self.last_move = 2
                self.move_direction(Direction.WEST)
            elif move == 3:
                self.last_move = 3
                self.move_direction(Direction.EAST)  
            self.new_direction = False
        elif self.new_direction is False:
            if self.last_move == 0:                
                self.move_direction(Direction.UP)
            elif self.last_move == 1:
                self.move_direction(Direction.DOWN)
            elif self.last_move == 2:
                self.move_direction(Direction.WEST)
            elif self.last_move == 3:
                self.move_direction(Direction.EAST)  
        self.attempts += 1

    def run(self):
        """
            Runs the rule-based controller
        """
        self.last_move = None #The previous move in this attempt
        self.attempts = 0
        self.new_direction = True
        self.attempt_threshold = int(5/self.agent.velocity)
        total_frames = self.calculate_frames()
        for i in range(total_frames):
            sensors_result = self.check_all_distance_sensors()
            sensor_flag = False
            for i in sensors_result:
                if isinstance(i, float) and i < 1:
                    sensor_flag = True

            # If something is in the sensor, change rules
            if sensor_flag:
                if self.agent.init_volume > 1 and self.agent.morph_index == 0:
                    self.morph(1)
                elif self.agent.init_volume > 1 and self.agent.morph_index == len(self.agent.morphs)-1:
                    self.morph(-1)
                elif self.agent.init_volume > 1 and self.check_percent_distance_sensors() == .4 or self.check_percent_distance_sensors() == .6:
                    #Under the assumption that the preset sensor choice is being used
                    if (self.check_distance_sensor(0) < 1 and self.check_distance_sensor(3) < 1):
                        if not self.morph(-1):
                            self.move_direction(Direction.WEST)
                    elif (self.check_distance_sensor(1) < 1 and self.check_distance_sensor(4) < 1):
                        if not self.morph(-1):
                            self.move_direction(Direction.EAST)
                    elif (self.check_distance_sensor(0) < 1 and self.check_distance_sensor(1) < 1):
                        if not self.morph(1):
                            self.move_direction(Direction.UP)
                    elif (self.check_distance_sensor(3) < 1 and self.check_distance_sensor(4) < 1):
                        if not self.morph(1):
                            self.move_direction(Direction.DOWN)
                else:
                    self.move_side()
            # Otherwise, keep moving forward
            else:
                self.new_direction = True
                self.attempts = 0               
                self.move_direction(Direction.NORTH)
