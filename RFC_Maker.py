class Cavity:

    settings = {
        "name" : "OUTPUT",
        "title": "RF cavity",
        "freq": 1000.0,
        "beta": 1.0,
        "E0": 1000000.0,
        "rmass": 0.551,
        "BoundaryConditions": {"up": 1, "right": 1, "left": 1, "low": 0},
        "cell_length": 0.0,
        "cell_radius": 0.0,
        "bp_length": 0.0,
        "bp_radius": 0.0
    }
    def __init__(self):
        return self
        
    
    def draw(self):
        """Return a list of points wich will be used to generate the Autofish file."""
        coordinates = (
            (0, 0),
            (0, self.settings["cell_radius"]),
            (self.settings["cell_length"], self.settings["cell_radius"]),
            (self.settings["cell_length"], self.settings["bp_radius"]),
            (self.settings["cell_length"] + self.settings["bp_length"], self.settings["bp_radius"]),
            (self.settings["cell_length"] + self.settings["bp_length"], 0),
            (0, 0)
            )
        return coordinates
    
    def generate(self):
        self.settings["drive point"] = (self.settings["cell_length"]/2, self.settings["cell_radius"]/2)
        filename = f"{self.settings["name"]}.af"
        header = f"{self.settings["title"]}\n\n$reg kprob = 1, \ndx = .2,\nfreq = {self.settings["freq"]},\nbeta = {self.settings["beta"]},\nezero = {self.settings["E0"]},\nrmass = {self.settings["rmass"]},\nnbsup = {self.settings["BoundarieConditions"]["up"]},\nnbslo = {self.settings["BoundarieConditions"]["low"]},\nnbsrt = {self.settings["BoundarieConditions"]["right"]},\nnbslf = {self.settings["BoundarieConditions"]["left"]},\nxdri = {self.settings["drive point"][0]},\nydri = {self.settings["drive point"][1]},\nclength = {self.settings["cell_length"]} $\n\n"
        coordinates = self.draw()
        with open(filename, "w") as f:
            f.write(header)
            for coordinate in coordinates:
                f.write(f"$po x={coordinate[0]},y={coordinate[1]}")
            