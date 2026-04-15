paths = {
        "A":[
            {"name": "+1 Orb", "cost": 0, "multishot": 2, "homing": False, "shoot_delay": 30},
            {"name": "+1 More Orb", "cost": 0,"multishot": 3, "homing": False, "shoot_delay": 30},
            {"name": "+2 Orbs", "cost": 0, "multishot": 5, "homing": False, "shoot_delay": 30},
            {"name": "+10 Orbs!", "cost": 0, "multishot": 15, "homing": False, "shoot_delay": 15}],
        "B": [
            {"name": "Faster Shooting", "cost": 0, "multishot": 1, "homing": False, "shoot_delay": 15},
            {"name": "Homing Orbs", "cost": 0, "multishot": 1, "homing": True, "shoot_delay": 15},
            {"name": "2 Homing Orbs?", "cost": 0, "multishot": 2, "homing": True, "shoot_delay": 15},
            {"name": "3 Homing Orbs!", "cost": 0, "multishot": 3, "homing": True, "shoot_delay": 15}]
}

def apply_upgrade(player, path_key):
    path = paths[path_key]
    tier = player.path_tiers[path_key]

    if tier >= len(path):
        return False
    upgrade = path[tier]
    
    if player.score < upgrade["cost"]:
        return False
    
    player.score -= upgrade["cost"]
    player.multishot = upgrade["multishot"]
    player.shoot_delay = upgrade["shoot_delay"]
    player.homing = upgrade["homing"]

    player.path_tiers[path_key] += 1
    return True




