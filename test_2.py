from trafficSimulator import *

# Create simulation
sim = Simulation()

# Add multiple roads
sim.create_roads([
    ((0, 100), (150, 100)),
    ((150, 100), (300, 100)),
    
    ((150, 0), (150, 100)),
    ((150, 100), (150, 200)),

    ((149.99,99.99),(150,100))

])

sim.create_gen({
    'vehicle_rate': 100,
    'vehicles': [
        [1, {"path": [0, 4, 1]}],
        [1, {"path": [0, 4, 3]}],
        [1, {"path": [2, 4, 3]}],
        [1, {"path": [2, 4, 1]}]
    ]
})


# Start simulation
win = Window(sim)
win.offset = (-150, -110)
win.run(steps_per_update=5)