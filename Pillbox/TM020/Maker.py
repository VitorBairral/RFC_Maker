class Cavity:
    """This module is designed to generate Autofish input codes in order to 
        automatize simulations of RF cavities. All parameters are written in the
        same way of Autofish code. You shall pass the parameters of the cavity, 
        such as it geometry through a dictionary with this structure (just copy this dictionary and insert your values (: ):\n
            settings = {
                "name" : <str>, #Sets the name of the output file
                "title": <str>, #Sets the title of the simulated mesh
                "thickness": <float>, #Sets the dx value. Use small values for a thin mesh. Thin meshes give you more accurate results, but spends more processing 
                "freq": <float>, #Sets the initial frequency of the simulation
                "beta": <float>, #Sets the particle speed in relation to the speed of light
                "norm": <int>, #Sets the field normalization type. 0 for EZERO normalization, 1 for EZEROT normalization  
                "clength": <float>, #Sets the CLENGTH value using in NORM=0
                "E0": <float>, #Sets the value of the initial electric field inside the cavity for NORM=0
                "E0T": <float>, #Sets the value of the acceleration electric field for NORM=1
                "rmass": <float>, #Sets the relativistic mass of the particle
                "BoundaryConditions": {"up": 1, "right": 1, "left": 1, "low": 0}, #Sets the boundary condition of the simulation (don't recommended to change this parameter)
                "cell_length": <float>,
                "cell_radius": <float>,
                "bp_length": <float>, #Beampipe length (the beampipe is required to simulate the side walls of cavity)
                "bp_radius": <float> #Beampipe radius.
                "full": <bool> #Simulates the full cavity or half of the cavity. Half-cavities are lighter to simulate, but keep in mind that values that depends of the energy in the cavity depend of the area of the cavity.
    }
    The drive point of the simulation is automatically located at the center of the cell.
    The zctr point is automatically located at the center of the cavity (not needed in half cavities).
    To insert the the settings of the cavity, use the function Cavity.fit(parameter_dictionary)
    To generate the Autofish input file, use the method Cavity.generate()
    """

    def fit(self, params):
        self.settings = params
    def __draw(self):
        coordinates = ""
        if self.settings["full"]:
            coordinates = f"""$po x=0,y=0 $
                $po x=0,y={self.settings["bp_radius"]} $
                $po x={self.settings["bp_length"]},y={self.settings["bp_radius"]} $
                $po x={self.settings["bp_length"]},y={self.settings["cell_radius"]} $
                $po x={self.settings["cell_length"] + self.settings["bp_length"]},y={self.settings["cell_radius"]} $
                $po x={self.settings["cell_length"] + self.settings["bp_length"]},y={self.settings["bp_radius"]} $
                $po x={self.settings["cell_length"] + 2 * self.settings["bp_length"]},y={self.settings["bp_radius"]} $
                $po x={self.settings["cell_length"] + 2 * self.settings["bp_length"]},y=0 $
                $po x=0,y=0 $"""
        else:
            coordinates = f"""$po x=0,y=0 $
                $po x=0,y={self.settings["cell_radius"]} $
                $po x={self.settings["cell_length"]/2},y={self.settings["cell_radius"]} $
                $po x={self.settings["cell_length"]/2},y={self.settings["bp_radius"]} $
                $po x={self.settings["cell_length"]/2 + self.settings["bp_length"]},y={self.settings["bp_radius"]} $
                $po x={self.settings["cell_length"]/2 + self.settings["bp_length"]},y=0$
                $po x=0,y=0 $"""
        return coordinates
    def generate(self):
        zctr = 0
        if self.settings["full"]:
            cavity_length = self.settings["cell_length"] + 2 * self.settings["bp_length"]
            zctr = cavity_length / 2
            
        else:
            cavity_length = self.settings["cell_length"]
        fclength = cavity_length / 2
        header = f"""{self.settings["title"]}
            $reg kprob=1,
            kmethod=1,
            dx={self.settings["thickness"]},
            freq={self.settings["freq"]},
            beta={self.settings["beta"]},
            norm={self.settings["norm"]},
            clength={self.settings["clength"]}
            ezero={self.settings["E0"]},
            ezerot={self.settings["E0T"]}
            rmass={self.settings["rmass"]},
            nbsup = {self.settings["BoundaryConditions"]["up"]},
            nbslo = {self.settings["BoundaryConditions"]["low"]},
            nbsrt = {self.settings["BoundaryConditions"]["right"]},
            nbslf = {self.settings["BoundaryConditions"]["left"]},
            xdri={fclength/2},
            ydri={self.settings["cell_radius"]/2},
            zctr={zctr}$
            """        
        coordinates = self.__draw()
        with open(f"{self.settings["name"]}.af", "w") as f:
            f.write(header)
            f.write(coordinates)

        