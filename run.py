from agent import Agent
from world import World
import time, datetime, os
from Sensors.distance_sensor import DistanceSensor
from direction import Direction
from Controllers.base_controller import BaseController
from Controllers.random_controller import RandomController
from Controllers.rule_based_controller import RuleBasedController
from Controllers.demo_morph_controller import DemoMorphController

def run():
    start = time.time()
    seconds = 60.0
    frame_time = 0.1

    my_time = datetime.datetime.now()
    file_name = (my_time.strftime("%m-%d-%Y %I.%M.%S%p"))
    log_file = "Log Files/" + file_name + ".dat"

    agent1 = Agent(0, 5, 5, 3)
    agent1.generate_preset_sensors()
    world = World(log_file, seconds, frame_time, agent1, 100, 11, 11, 10)

    controller = RuleBasedController(log_file, world, agent1, seconds, frame_time)

    print(controller.world.gap_coords)

    controller.run()
    return tuple((controller.steps_taken, time.time()-start))

os.remove("Stats.txt")
stats_file = open("Stats.txt", "w")

trails = 1

for i in range(trails):
    data = run()
    stats_file.write(str(i) + " " + str(data[0]) + " " + str(data[1]) + "\n")

stats_file.close()


