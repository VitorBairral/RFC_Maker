from numpy import sin, cos, tan, deg2rad
class Cavity:
    """This module is designed to generate Autofish input codes containing the code for an half-cell cavity in order to 
        automatize simulations of RF cavities. All parameters are written in the
        same way of Autofish code. You shall pass the parameters of the simulation,  
        the cavity geometry, nose cone and beampipe, if there is, through dictionaries that follows the following structure:\n
            settings = {  # Sets the simulation parameters
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
            }
            cavity = { # Sets the cavity parameters
                "radius": <float>,
                "length": <float>,
                "c_rad": <float>, # This parameter sets how smooth are the cavity corners. The corners are described as circle quarters. This parameter gives the ratio between the cell length and the circle quarter radius. If 0, the corner will not be smoothed. Standard set as 0
                "reintrance": sets the parameter of the HOM damper slot. <dict> {"height": sets the position of the slot in the cell wall <float>, "width": sets the slot opening size. <float>, "depth": sets the slot depth <float>}
            }
            beampipe = { # Sets the beampipe parameters (Optional, but highly recommended to use)
                "radius": <float>,
                "length": <float>,
                "smooth": <float> [0,1] # This parameter sets how smooth is the connection between the beampipe and cell. This connection is described as a circle quarter. This parameter gives the ratio between the beampipe radius and the circle quarter radius. If 0, the corner will not be smoothed. Not needed if the cavity have a nose cone. Standart set as 0.
            }
            nose_cone = { # Sets the nose cone parameters. More explanation in module documentation
                "length": <float>, # The distance between the cavity wall and the nose cone vertex
                "i_rad": <float>, # The radius of the inner circle arc of the nose cone
                "o_rad": <float>, # The  radius of the outer circle arc of the nose cone
                "theta": <float> # The aperture angle of the nose cone.
            }
            
    The drive point of the simulation is automatically located at the center of the cell.
    The zctr point is automatically located at the center of the cavity (not needed in half cavities).
    To insert the the settings of the cavity, use the function Cavity.fit(parameter_dictionary)
    To generate the Autofish input file, use the method Cavity.generate()
    """
    def __init__(self):
        self.coordinates = []

    def fit(self, sim_params, cav_params, beampipe=None, nose_cone=None):
        point = {
            "nt": 0,
            "x0": 0,
            "y0": 0,
            "x": 0,
            "y": 0
        }
        self.settings = sim_params 
        self.cavity = cav_params
        self.beampipe = beampipe
        self.nose_cone = nose_cone
        self.coordinates.append(point)    
    def __draw_bp(self):
        point = {
            "nt": 0,
            "x0": 0,
            "y0": 0,
            "x": 0,
            "y": 0
        }
        if self.beampipe["length"] != 0:
            point["x"] = self.beampipe["length"] + self.cavity["length"]
            point["y"] = 0
            self.coordinates.append(point.copy())
            point["x"] = self.beampipe["length"] + self.cavity["length"]
            point["y"] = self.beampipe["radius"]
            self.coordinates.append(point.copy())
            point["x"] = self.cavity["length"]
            self.coordinates.append(point.copy())
    
    def __draw_nose(self):
        point = {
            "nt": 0,
            "x0": 0,
            "y0": 0,
            "x": 0,
            "y": 0,
            "r": 0,
            "t": 0
        }
        t = self.nose_cone["theta"]
        rt = deg2rad(t)
        r = self.nose_cone["i_rad"]
        R = self.nose_cone["o_rad"]
        cx = self.cavity["length"] - self.nose_cone["length"] + r 
        cy = self.beampipe["radius"] + r 

        x1 = -1 * sin(rt) * r 
        y1 = cos(rt) * r 

        x0 = self.nose_cone["length"] - R - r #r2 center
        x2 = sin(rt)*R + x0
        y0 = x2*tan(rt) + r * (1/cos(rt)) + cos(rt)*R # r2 center
        y2 = y0 - cos(rt)*R 

        point["x"] = cx
        point['y'] = self.beampipe["radius"]
        self.coordinates.append(point.copy())

        point["nt"] = 5
        point["r"] = r 
        point['x0'] = cx
        point['y0'] = cy
        point['x'] = x1
        point["y"] = y1 
        self.coordinates.append(point.copy())

        point["nt"] = 0
        point["x"] = cx + x2
        point["y"] = cy + y2
        self.coordinates.append(point.copy())

        point["nt"] = 2
        point["x0"] = self.cavity["length"] - R
        point["y0"] = y0 + cy
        point["x"] = R
        point["y"] = 0
        point["r"] = R 
         
        self.coordinates.append(point.copy())
    
    def __draw_cav(self):

        point = {
            "nt": 0,
            "x0": 0,
            "y0": 0,
            "x": 0,
            "y": 0,
            "r": 0,
            "t": 0
        }
        if "reintrance" in self.cavity.keys():
            point["x"] = self.cavity["length"]
            point["y"] = self.cavity["reintrance"]["height"] - 0.1
            self.coordinates.append(point.copy())

            point["nt"] = 2
            point["x0"] = self.cavity["length"] + 0.1
            point["y0"] = self.cavity["reintrance"]["height"] - 0.1
            point["x"] = 0
            point["y"] = 0.1
            point["r"] = 0.1
            self.coordinates.append(point.copy())
        
            point["nt"] = 0 
            point["x"] = self.cavity["length"] + self.cavity["reintrance"]["depth"]
            point["y"] = self.cavity["reintrance"]["height"]
            self.coordinates.append(point.copy())

            point["y"] += self.cavity["reintrance"]["width"]
            self.coordinates.append(point.copy())

            point["x"] = self.cavity["length"] + 0.1
            self.coordinates.append(point.copy())

            point["nt"] = 2
            point["x0"] = self.cavity["length"] + 0.1
            point["y0"] = point["y"] + 0.1
            point["x"] = -0.1
            point["y"] = 0
            self.coordinates.append(point.copy())

        point["nt"] = 0
        point["x"] = self.cavity["length"]
        point["y"] = self.cavity["radius"] - self.cavity["c_rad"]
        self.coordinates.append(point.copy())

        point["nt"] = 2
        point["r"] = self.cavity["c_rad"]
        point["x0"] = self.cavity["length"] - self.cavity["c_rad"]
        point['y0'] = self.cavity["radius"] - self.cavity["c_rad"]
        point["x"] = 0
        point["y"] = self.cavity["c_rad"]
        self.coordinates.append(point.copy())

        point["nt"] = 0 
        point["x"] = 0
        point["y"] = self.cavity["radius"]
        self.coordinates.append(point.copy())

        point = {
            "nt": 0,
            "x0": 0,
            "y0": 0,
            "x": 0,
            "y": 0,
            "r": 0,
            "t": 0
        }
        self.coordinates.append(point)

    def generate(self):
        if self.beampipe["length"]:
            self.__draw_bp()
        if self.nose_cone["length"]:
            self.__draw_nose()
        self.__draw_cav()
        points = ""
        for point in self.coordinates:
            if point["nt"] == 0:
                points += f"$po x={point["x"]}, y={point["y"]}$\n"
            else:
                points += f"$po nt={point["nt"]}, x0={point["x0"]}, y0={point["y0"]}, x={point["x"]}, y={point["y"]}, radius={point["r"]}$\n"
        zctr = self.settings["clength"] * 0.5
        header = f"""{self.settings["title"]}
            $reg kprob=1,
            kmethod=1,
            dx={self.settings["thickness"]},
            dy={self.settings["thickness"]},
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
            zctr={zctr}$\n"""        
        with open(f"{self.settings["name"]}.af", "w") as f:
            f.write(header)
            f.write(points)

        