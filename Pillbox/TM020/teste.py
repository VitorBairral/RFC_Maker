import Maker 
import os
import time
cav = Maker.Cavity()
settings = {
        "name" : "020 Sirius Pillbox", #Sets the name of the output file
        "thickness" : 0.1,
        "title": "TM 020 500 MHz Pillbox", #Sets the title of the simulated mesh
        "freq": 500, #Sets the initial frequency of the simulation
        "beta": 1, #Sets the particle speed in relation to the speed of light
        "norm" : 1,
        "E0T" : 1666666.66,
        "clength" : 15, 
        "E0": 2617993.8779914943, #Sets the value of the initial electric field inside the cavity
        "rmass": 0.511, #Sets the relativistic mass of the particle
        "BoundaryConditions": {"up": 1, "right": 1, "left": 1, "low": 0}, #Sets the boundary condition of the simulation (don't recommended to change this parameter)
        "cell_length": 30.0,
        "cell_radius": 52.71,
        "bp_length": 24.0, #Beampipe length (the beampipe is required to simulate the side walls of cavity)
        "bp_radius": 1.2, #Beampipe radius.
        "full": False, #Simulates the full cavity or half of the cavity. Half-cavities are lighter to simulate, but keep in mind that values that depends of the energy in the cavity depend of the area of the cavity.
        
    }
def tester(x_max, y_max, step, step_raio):
    start_x = 1.0
    start_y = 1.0
    while start_y <= y_max:
        while start_x <= x_max:
            settings["bp_length"] = start_x
            settings["bp_radius"] = start_y
            settings["name"] = f"({float(start_x)}, {float(start_y)})"
            
            cav.fit(settings)
            cav.generate()
            nome_af = settings["name"] + ".af"
            os.startfile(nome_af)
            time.sleep(15 + (start_x * start_y)/10)
            start_x += step
            print(f"{settings["name"]}.SFO gerado")
        start_x = 1
        start_y += step_raio
        
def deletar():
    diretorio = r"c:\Users\vitor25023\Documents\Teste em lote\Teste TM020"
    for arquivo in os.listdir(diretorio):
        if ".py" not in arquivo and ".SFO" not in arquivo:
            caminho = os.path.join(diretorio, arquivo)
            os.remove(caminho)

tester(25, 5, 0.5, 1)


