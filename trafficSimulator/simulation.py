from .road import Road
from copy import deepcopy
from .vehicle_generator import VehicleGenerator
import random

class Simulation:
    def __init__(self, config={}):
        # Set default configuration
        self.set_default_config()

        # Update configuration
        for attr, val in config.items():
            setattr(self, attr, val)

    def set_default_config(self):
        self.t = 0.0            # Time keeping
        self.frame_count = 0    # Frame count keeping
        self.cars_started = 0
        self.cars_finished = 0
        self.cars_live = 0
        self.dt = 1/60          # Simulation time step
        self.roads = []         # Array to store roads
        self.generators = []
        self.total_time = 0.0
        self.avg_time = 0.0

        self.car_list = {}

    def update_number_of_vechicles(self):
        self.cars_started += 1

    def create_road(self, start, end):
        road = Road(start, end)
        self.roads.append(road)
        return road

    def create_roads(self, road_list):
        for road in road_list:
            self.create_road(*road)

    def add_car_number_update(self):
        self.cars_started += 1

    def create_gen(self, config={}):
        gen = VehicleGenerator(self, config, )
        self.generators.append(gen)
        return gen

    def update(self):
        # Update every road
        for road in self.roads:
            road.update(self.dt)

        # Add vehicles
        for gen in self.generators:
            gen.update()
        
        # Check roads for out of bounds vehicle
        for road in self.roads:
            # If road has no vehicles, continue
            if len(road.vehicles) == 0: continue

            for i in range(1, len(road.vehicles)):
                road.vehicles[i].update(road.vehicles[i-1], self.dt)

            #add to list cars every first vechicle on the road    
            self.car_list[road.vehicles[-1].car_id] = road.vehicles[-1] 
            # If not
            vehicle = road.vehicles[0]
            # If first vehicle is out of road bounds
            if vehicle.x >= road.length:                # If vehicle has a next road
                if vehicle.current_road_index + 1 < len(vehicle.path):
                    # Update current road to next road
                    vehicle.current_road_index += 1
                    # Create a copy and reset some vehicle properties
                    new_vehicle = deepcopy(vehicle)
                    new_vehicle.x = 0
                    # Add it to the next road
                    #TODO: add only if there is a space 
                    next_road_index = vehicle.path[vehicle.current_road_index]
                    
                    if len(self.roads[next_road_index].vehicles) != 0:
                        #print(self.roads[next_road_index].vehicles[-1].x, self.roads[next_road_index].vehicles[-1].l)
                        if self.roads[next_road_index].vehicles[-1].x > self.roads[next_road_index].vehicles[-1].l:
                            self.roads[next_road_index].vehicles.append(new_vehicle)
                            self.car_list[vehicle.car_id] = vehicle
                            self.car_list.pop(vehicle.car_id)
                            road.vehicles.popleft()
                        else:
                          vehicle.unstop()
                    else:
                        self.roads[next_road_index].vehicles.append(new_vehicle)
                        self.car_list[vehicle.car_id] = vehicle
                        self.car_list.pop(vehicle.car_id)
                        road.vehicles.popleft()
                else:
                    self.cars_finished += 1
                    self.total_time += self.t - vehicle.sim_time
                    self.car_list.pop(vehicle.car_id)
                    road.vehicles.popleft()
                # In all cases, remove it from its road
                
               
            elif vehicle.x > road.length - 1.5 * vehicle.l :
                next_road_index = vehicle.path[vehicle.current_road_index]
                if next_road_index < len(vehicle.path) - 2:
                    if len(self.roads[next_road_index].vehicles) != 0 and self.roads[next_road_index].vehicles[-1].x < self.roads[next_road_index].vehicles[-1].l:
                        vehicle.stop()
                        vehicle.unslow()
                    else: 
                        vehicle.unslow()
            elif vehicle.x > road.length - 3 * vehicle.l:
                next_road_index = vehicle.path[vehicle.current_road_index ]
                if next_road_index < len(vehicle.path) - 2:
                    if len(self.roads[next_road_index].vehicles) != 0 and self.roads[next_road_index].vehicles[-1].x < 3 * self.roads[next_road_index].vehicles[-1].l:
                        vehicle.slow(vehicle.v_max * 0.3)
            elif vehicle.x > road.length - 7 * vehicle.l:
                next_road_index = vehicle.path[vehicle.current_road_index]
                if next_road_index < len(vehicle.path) - 2:
                    if len(self.roads[next_road_index].vehicles) != 0 and self.roads[next_road_index].vehicles[-1].x < 7 * self.roads[next_road_index].vehicles[-1].l:
                        vehicle.slow(vehicle.v_max * 0.7)

        # Increment time
        self.t += self.dt
        self.frame_count += 1
        self.cars_live = self.cars_started - self.cars_finished
        if self.cars_finished == 0:
            self.avg_time = 0.0
        else:    
            self.avg_time =  self.total_time / self.cars_finished

        if self.t > 120 and self.t <= 120 + self.dt :
            print(self.avg_time)
            



    def run(self, steps):
        for _ in range(steps):
            self.update()