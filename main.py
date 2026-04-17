class Action:
    def __init__(self, name, energy_cost, damage, shield_gain):
        
        # Validation
        
        if name == "":
            raise ValueError("action name must not be empty")
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

        if name == "":
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
    
        absorbed = min(self.shield, amount)
        self.shield -= absorbed
        remaining = amount - absorbed
        self.health = max(0, self.health - remaining)

        return remaining

    def is_defeated(self):
        if self.health <= 0:
            return True
        return False

    def get_status(self): 
        return {
            "name": self.name,
            "health": self.health,
            "energy": self.energy,
            "shield": self.shield,
        }

class TurnRecord:
    def __init__(self, turn_number, actor_name, target_name, action_name, shield_gain, damage, damage_dealt):
        self.turn_number = turn_number
        self.actor_name = actor_name
        self.target_name = target_name
        self.action_name = action_name
        self.shield_gain = shield_gain
        self.damage = damage
        self.damage_dealt = damage_dealt

    def summary(self):
        return(f"{self.turn_number}. {self.actor_name} used {self.action_name} on {self.target_name}: +{self.shield_gain} shield, {self.damage} damage, {self.damage_dealt} dealt")


class Battle:
    def __init__(self, left_fighter, right_fighter):

        if left_fighter.name == right_fighter.name:
            raise ValueError("fighter names must be different")
            
        self.left_fighter = left_fighter
        self.right_fighter = right_fighter
        self.current_turn = left_fighter.name
        self.history = []

    def take_turn(self, actor_name, action):
        if self.is_finished():
            raise ValueError("Battle is already finished")
        if actor_name != self.current_turn:
            raise ValueError("Wrong turn")

        if actor_name == self.left_fighter.name:
            actor = self.left_fighter
            target = self.right_fighter
        else:
            actor = self.right_fighter
            target = self.left_fighter

        if actor.energy < action.energy_cost:
            raise ValueError(f"{actor.name} does not have enough energy for {action.name}")

        actor.spend_energy(action.energy_cost)

        if action.shield_gain > 0:
            actor.gain_shield(action.shield_gain)

        damage_dealt = 0
        if action.damage > 0:
            damage_dealt = target.receive_damage(action.damage)

        actor.gain_energy(1)
        target.gain_energy(1)

        turn_number = len(self.history) + 1
        record = TurnRecord(
            turn_number=turn_number,
            actor_name=actor.name,
            target_name=target.name,
            action_name=action.name,
            shield_gain=action.shield_gain,
            damage=action.damage,
            damage_dealt=damage_dealt,
        )
        self.history.append(record)

        if self.is_finished():
            self.current_turn = None
        else:
            self.current_turn = target.name

        return record

    def is_finished(self):
        if self.left_fighter.health <= 0 or self.right_fighter.health <= 0:
            return True
        return False

    def winner_name(self):
        if not self.is_finished():
            return None
        if self.left_fighter.health <= 0 and self.right_fighter.health <= 0:
            return None
        if self.left_fighter.health <= 0:
            return self.right_fighter.name
        return self.left_fighter.name

    def get_status(self):
        return {
            "finished": self.is_finished(),
            "winner": self.winner_name(),
            "current_turn": self.current_turn,
            "turns": len(self.history),
            "left": self.left_fighter.get_status(),
            "right": self.right_fighter.get_status(),
        }

    def get_report(self):
        winner = self.winner_name()
        winner_text = "none" if winner is None else winner

        next_turn_text = "none" if self.current_turn is None else self.current_turn

        left = self.left_fighter
        right = self.right_fighter

        lines = [
            f"Winner: {winner_text}",
            f"Turns: {len(self.history)}",
            f"Next turn: {next_turn_text}",
            f"{left.name} - HP: {left.health}, Energy: {left.energy}, Shield: {left.shield}",
            f"{right.name} - HP: {right.health}, Energy: {right.energy}, Shield: {right.shield}",
            "History:",
        ]
        lines.extend(record.summary() for record in self.history)
        return "\n".join(lines)
