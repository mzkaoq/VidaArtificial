from trafficSimulator import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([
    ((0, 100), (150, 100)),
    ((150, 100), (300, 100)),
    
    ((150, 0), (150, 100)),
    ((150, 100), (150, 200)),

    # ((149.99,99.99),(150,100))

])


sim.create_gen({
    'gen_id': 1,
    'vehicle_rate': 10,
    'vehicles': [
        [1, {"path": [0, 1]}],
        [1, {"path": [0, 3]}],
        [1, {"path": [2, 3]}],
        [1, {"path": [2, 1]}]
    ]
})


# Start simulation
win = Window(sim)
win.offset = (-150, -100)
win.run(steps_per_update=5) 

