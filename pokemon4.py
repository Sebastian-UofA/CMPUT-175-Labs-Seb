import random

class Pokemon:
    def __init__(self, name, attack, defense, max_health, current_health):
        self.name = name
        self.attack = attack
        self.defense = defense
        self.max_health = max_health
        self.current_health = current_health

    def __str__(self) -> str:
        """
        Return a string representation of the Pokemon.
        """

        return f"{self.name} (health: {self.current_health}/{self.max_health})"

    def lose_health(self, amount: int) -> None:
        """
        Lose health from the Pokemon.
        """
        if amount > 0:
            self.current_health = max(0, self.current_health - amount)

    def is_alive(self) -> bool:
        """
        Return True if the Pokemon has health remaining.
        """
        return self.current_health > 0

    def revive(self) -> None:
        """
        Revive the Pokemon.
        """
        self.current_health = self.max_health
        print(f"{self.name} has been revived!")

    def attempt_attack(self, other: "Pokemon") -> bool:
        """
        Attempt an attack on another Pokemon.
        """
        coefficient_of_luck = random.choice([0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3])
        damage = round(self.attack * coefficient_of_luck)

        if damage > other.defense:
            other.lose_health(damage - other.defense)
            print(f"{self.name} attacks {other.name} for {damage} damage!")
            if not other.is_alive():
                if random.choice([True, False]):  # 50% chance of revival
                    other.revive()
                    
        else:
            print(f"{self.name} attacks {other.name} for {damage} damage!")
            print(f"Attack is blocked!")

        return damage > other.defense


def read_pokemon_from_file(filename: str) -> list[Pokemon]:
    """
    Read a list of Pokemon from a file.
    """
    pokemon_list = []
    with open(filename, "r", encoding="utf-8") as file:
        next(file)  # Skip the header line
        for line in file:
            name, attack, defense, health = map(str.strip, line.split('|'))
            pokemon = Pokemon(name, int(attack), int(defense), int(health), int(health))
            pokemon_list.append(pokemon)
    return pokemon_list

def main():
    """
    Battle of two Pokemon with simulation.
    """
    all_pokemon = read_pokemon_from_file("all_pokemon.txt") # Read Pokemon from the file

    pokemon1, pokemon2 = random.sample(all_pokemon, 2)  # Randomly select two different Pokemon

    print(f"Welcome, {pokemon1} and {pokemon2}!\n")

    round_count = 1

    while pokemon1.is_alive() and pokemon2.is_alive() and round_count <= 10:
        print(f"Round {round_count} begins! {pokemon1} and {pokemon2}")

        # Pokemon 1 attacks Pokemon 2
        if pokemon1.attempt_attack(pokemon2):
            print(f"Attack is successful! {pokemon2.name} has {pokemon2.current_health} health remaining!")
            if not pokemon2.is_alive():
                if random.choice([True, False]):  # 50% chance of revival
                    pokemon2.revive()
                    

        # Check if Pokemon 1 is still alive before allowing Pokemon 2 to attack
        if pokemon1.is_alive():
            # Pokemon 2 attacks Pokemon 1
            if pokemon2.is_alive() and pokemon2.attempt_attack(pokemon1):
                print(f"Attack is successful! {pokemon1.name} has {pokemon1.current_health} health remaining!")
                if not pokemon1.is_alive():
                    if random.choice([True, False]):  # 50% chance of revival
                        pokemon1.revive()
                        

        print()

        round_count += 1

    print(f"The battle ends in a tie between {pokemon1.name} (health: {pokemon1.current_health}/{pokemon1.max_health}) and {pokemon2.name} (health: {pokemon2.current_health}/{pokemon2.max_health})" if pokemon1.is_alive() and pokemon2.is_alive()
          else f"{pokemon1.name} (health: {pokemon1.current_health}/{pokemon1.max_health}) has won in {round_count - 1} rounds!" if pokemon1.is_alive()
          else f"{pokemon2.name} (health: {pokemon2.current_health}/{pokemon2.max_health}) has won in {round_count - 1} rounds!")

if __name__ == "__main__":
    main()

