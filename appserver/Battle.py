class Battle:
    def __init__(self):
        self.nb_moves = 10
        self.rules = {}

    def load_file(self, filepath):
        """Parse un fichier .battle et charge les règles."""
        current_color = None

        with open(filepath, "r") as f:
            for raw_line in f:
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                if line.startswith("MVS"):
                    self.nb_moves = int(line.split()[1])
                    continue

                if line.startswith("[") and line.endswith("]"):
                    current_color = line[1:-1]
                    self.rules[current_color] = []
                    continue

                if current_color and "=" in line:
                    left, pts = line.rsplit("=", 1)
                    points = int(pts)
                    left = left.strip()

                    if "+" in left:
                        actions = [k.strip() for k in left.split("+")]
                        self.rules[current_color].append({
                            "type": "AND",
                            "actions": actions,
                            "points": points
                        })
                    elif "," in left:
                        actions = [k.strip() for k in left.split(",")]
                        self.rules[current_color].append({
                            "type": "OR",
                            "actions": actions,
                            "points": points
                        })
                    else:
                        self.rules[current_color].append({
                            "type": "SINGLE",
                            "actions": [left],
                            "points": points
                        })

        print(f"[.battle] {self.nb_moves} mouvements | couleurs : {list(self.rules.keys())}")

    def calcul_step_score(self, col: str, arm: str, exp: str) -> int:
        """Calcule les points d'un pas selon les règles chargées."""
        if col not in self.rules:
            return 0

        step_actions = set()
        if arm:
            for a in arm.split("+"):
                step_actions.add(a.strip())
        if exp:
            step_actions.add(exp.strip())

        total = 0
        for rule in self.rules[col]:
            if rule["type"] == "AND":
                if all(a in step_actions for a in rule["actions"]):
                    total += rule["points"]
            elif rule["type"] == "OR":
                if any(a in step_actions for a in rule["actions"]):
                    total += rule["points"]
            elif rule["type"] == "SINGLE":
                if rule["actions"][0] in step_actions:
                    total += rule["points"]

        return total