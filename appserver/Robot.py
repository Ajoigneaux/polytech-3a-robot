class Robot:
    def __init__(self, rid : str):
        self.rid = rid
        self.score = 0
        self.steps = []
        # self.ip = ""
        
    
    def add_step(self, col, arm, exp, pts):
        """Ajoute un pas et met à jour le score."""
        self.steps.append({"col": col, "arm": arm, "exp": exp, "pts": pts})
        self.score += pts
 
    def reset(self):
        """Remet à zéro le score et les pas pour une nouvelle battle."""
        self.score = 0
        self.steps = []
 
    def __repr__(self):
        return f"Robot({self.rid}, score={self.score}, steps={len(self.steps)})"
