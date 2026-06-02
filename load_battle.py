def load_battle_file(filepath):
    """Parse un fichier .battle et charge les règles dans battle_rules.
 
    rules = {
        "N": [{"type": "AND"|"OR"|"SINGLE", "keys": [...], "points": int}, ...],
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
                    keys = [k.strip() for k in left.split("+")]
                    rules[current_color].append({
                        "type": "AND",
                        "keys": keys,
                        "points": points
                    })
                elif "," in left:
                    # Opérateur OU : un seul point même si plusieurs présents
                    keys = [k.strip() for k in left.split(",")]
                    rules[current_color].append({
                        "type": "OR",
                        "keys": keys,
                        "points": points
                    })
                else:
                    # Élément unique
                    rules[current_color].append({
                        "type": "SINGLE",
                        "keys": [left],
                        "points": points
                    })
 
    battle_rules = rules
    print(f"[.battle] {nb_moves} mouvements | couleurs : {list(rules.keys())}")