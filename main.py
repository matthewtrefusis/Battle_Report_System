class Action:
    def __init__(self, name, energy_cost, damage, shield_gain):
        
        # Validation
        
        if name is "":
            raise ValueError("Name cannot be empty")
        if energy_cost < 1:
            raise ValueError("Energy Cost must be atleast 1")
        if damage < 0:
            raise ValueError("Damage must be atleast 0")
        if shield_gain < 0:
            raise ValueError("Shield Gain must be atleast 0")
        if damage ==0 and shield_gain == 0:
            raise ValueError("Damage and Shield Gain cannot both be 0")

        # Variable Declarations
        
        self.name = name
        self.energy_cost = energy_cost
        self.damage = damage
        self.shield_gain = shield_gain
        

class Fighter:
    def __init__(self, name, health, energy):
        
        # Validation

        if name is "":
            raise ValueError("Name cannot be empty")
        if health < 1:
            raise ValueError("Health must be atleast 1")
        if energy < 0:
            raise ValueError("Energy must be atleast 0")

        # Declarations

        self.name = name
        self.health = health
        self.energy = energy
        self.shield = 0

    def gain_shield(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.shield += amount

    def spend_energy(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.energy -= amount

    def gain_energy(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        self.energy += amount

    def receive_damage(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
        if amount > self._shield:
            self.shield = 0
            amount -= self.shield
        elif self.shield >= amount:
            self.shield -= amount
            amount -= self.shield
        self.energy -= amount

    def is_defeated(self):
        if self._health <= 0:
            return True
        return False

    def get_status(self):
        self.name = name, self.health = health, self.energy = energy, self.shield = 0


class TurnRecord:
    def __init__(self, turn_number, actor_name, target_name, action_name, shield_gain, damage, damage_dealt):
        

    def summary(self):
        return(f"{self.turn_number} {self.actor_name} used {action_name} on {self.target_name}: +{self.shield_gain} shield, {self.damage} damage, {self.damage_dealt} dealt")


class Battle:
    def __init__(self, left_fighter, right_fighter):
        self.left_fighter = left_fighter
        self.right_fighter = right_fighter
        self.current_turn = left_fighter.name
        self.history = []

    def take_turn(self, actor_name, action):
        pass

    def is_finished(self):
        pass

    def winner_name(self):
        pass

    def get_status(self):
        pass

    def get_report(self):
        pass

