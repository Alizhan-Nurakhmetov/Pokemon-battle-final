class Move:
    def __init__(self,power):
        """Set the moves base damage"""
        self.power = power
    def damage(self, attacker, defender):
        """Return the base damage"""
        return self.power
class Typemove(Move):
    def damage(self, attacker, defender):
        """Add 10 for a strong matchup"""
        strong = {("grass", "water"), ("water", "fire"), ("fire", "grass")}
        if (attacker["type"], defender["type"] in strong:
            return self.power + 10
        return self.power
def damage(attack, attacker, defender):
    """Get the damage for the chosen attack"""
    if attack == "Basic":
        return Move(10).damage(attacker, defender)
    if attack == "Type":
        return TypeMove(6).damage(attacker, defender)
    raise ValueError("Choose Basic or Type")
