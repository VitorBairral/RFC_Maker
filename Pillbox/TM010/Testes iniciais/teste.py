import Maker 
import os
import time
cav = Maker.Cavity()
settings = {
        "name" : "teste", #Sets the name of the output file
        "title": "teste", #Sets the title of the simulated mesh
        "freq": 500.0, #Sets the initial frequency of the simulation
        "beta": 1, #Sets the particle speed in relation to the speed of light
        "E0": 2617993.8779914943, #Sets the value of the initial electric field inside the cavity
        "rmass": 0.511, #Sets the relativistic mass of the particle
        "BoundaryConditions": {"up": 1, "right": 1, "left": 1, "low": 0}, #Sets the boundary condition of the simulation (don't recommended to change this parameter)
        "cell_length": 30.0,
        "cell_radius": 22.96,
        "bp_length": 1.0, #Beampipe length (the beampipe is required to simulate the side walls of cavity)
        "bp_radius": 1.0, #Beampipe radius.
        "full": False #Simulates the full cavity or half of the cavity. Half-cavities are lighter to simulate, but keep in mind that values that depends of the energy in the cavity depend of the area of the cavity.
    }
def tester(x_max, y_max, step):
    start_x = 1.0
    start_y = 1.0
    while start_y < y_max:
        while start_x < x_max:
            settings["bp_length"] = start_x
            settings["bp_radius"] = start_y
            settings["name"] = f"({start_x, start_y})"
            cav.fit(settings)
            cav.generate()
            start_x += step
        start_x = 1.0
        start_y += step

def tester_segundo(comprimento_max, step):
    i = 1.0
    while i <= comprimento_max:
        settings["bp_length"] = i
        settings["bp_radius"] = 2.5
        nome = f"({i}, 2.5)"
        settings["name"] = nome 
        cav.fit(settings)
        cav.generate()
        nome_c = nome + ".af"
        



