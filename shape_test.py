from Controllers.rule_based_controller import RuleBasedController
import random
import numpy
import datetime

class ShapeTest(RuleBasedController):
    def run_morph(self):
        test_move = True
        total_frames = self.calculate_frames()
        thick = 1

        if not test_move:
            for i in range(self.agent.init_volume):
                if self.agent.agent_height == 1:
                    thick = -1
                if self.agent.agent_width == 1:
                    thick = 1
                self.morph(thick)
        else: 
            self.last_move = None #The previous move in this attempt
            self.attempts = 0
            self.new_direction = True
            self.attempt_threshold = 5
            total_frames = self.calculate_frames()
            for i in range(total_frames):
                distance = self.check_distance_sensor(0)
                if distance < 1:
                    self.move_side()
                    if distance < 1:
                        self.move_side()
                    if self.agent.agent_height == 1:
                        thick = -1
                    if self.agent.agent_width == 1:
                        thick = 1
                    self.morph(thick)
                else:
                    self.new_direction = True
                    self.attempts = 0
                    self.last_move = None                
                    self.move_direction(Direction.NORTH)
                    if distance < 1:
                        self.move_side()
                    if self.agent.agent_height == 1:
                        thick = -1
                    if self.agent.agent_width == 1:
                        thick = 1
                    self.morph(thick)
            
        
        
        

#######

from agent import Agent
from world import World
from Sensors.distance_sensor import DistanceSensor
from direction import Direction

seconds = 5.0
frame_time = 0.1

agent1 = Agent(0, 5, 5, 2)
sensor1 = DistanceSensor(0, 5, 5, Direction.NORTH)
agent1.append_sensor(sensor1)

my_time = datetime.datetime.now()
file_name = (my_time.strftime("%m-%d-%Y %I.%M.%S%p"))
log_file = "Log Files/" + file_name + ".dat"

world = World(log_file, seconds, frame_time, agent1, 100, 11, 11, 10)
controller = ShapeTest(log_file, world, agent1, seconds, frame_time)
controller.run_morph()
