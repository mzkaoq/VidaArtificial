
from trafficSimulator import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([
    ((0, 100), (300, 100)),
   
])

sim.create_gen({
    'gen_id': 1,
    'vehicle_rate': 50,
    'vehicles': [
        [1, {"path": [0]}]
    ]
})


# Start simulation
win = Window(sim)
win.offset = (-150, -110)
win.run(steps_per_update=5)