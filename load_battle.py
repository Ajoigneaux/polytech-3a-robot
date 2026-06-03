def load_battle_file(filepath):
    """Parse un fichier .battle et charge les règles dans battle_rules.
 
    rules = {
        "N": [{"type": "AND"|"OR"|"SINGLE", "actions": [...], "points": int}, ...],
        ...
    }
    """
    global nb_moves, battle_rules
    rules = {}
    current_color = None
 
    with open(filepath, "r") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
 
            # Recuperation du nombre de movements
            if line.startswith("MVS"):
                nb_moves = int(line.split()[1])
                continue
 
            # Début d'une section couleur  [N], [B], [R]...
            if line.startswith("[") and line.endswith("]"):
                current_color = line[1:-1]
                rules[current_color] = []
                continue
 
            # Règle de points
            if current_color and "=" in line:
                left, pts = line.rsplit("=", 1)
                points = int(pts)
                left = left.strip()
 
                if "+" in left:
                    # Opérateur ET : tous les éléments doivent être présents
                    actions = [k.strip() for k in left.split("+")]
                    rules[current_color].append({
                        "type": "AND",
                        "actions": actions,
                        "points": points
                    })
                elif "," in left:
                    # Opérateur OU : un seul point même si plusieurs présents
                    actions = [k.strip() for k in left.split(",")]
                    rules[current_color].append({
                        "type": "OR",
                        "actions": actions,
                        "points": points
                    })
                else:
                    # Élément unique
                    rules[current_color].append({
                        "type": "SINGLE",
                        "actions": [left],
                        "points": points
                    })
 
    battle_rules = rules
    print(f"[.battle] {nb_moves} mouvements | couleurs : {list(rules.actions())}")



def calcul_step_score(col: str, arm: str, exp: str):
    """Calcule les points d'un pas selon les règles chargées."""
    if col not in battle_rules:
        return 0

    # Ensemble des step_actions présents dans ce pas
    step_actions = set()
    if arm:
        for a in arm.split("+"):
            step_actions.add(a.strip())
    if exp:
        step_actions.add(exp.strip())

    total = 0
    for rule in battle_rules[col]:
        if rule["type"] == "AND":
            if all(k in step_actions for k in rule["actions"]):
                total += rule["points"]

        elif rule["type"] == "OR":
            if any(k in step_actions for k in rule["actions"]):
                total += rule["points"]

        elif rule["type"] == "SINGLE":
            if rule["actions"][0] in step_actions:
                total += rule["points"]

    return total