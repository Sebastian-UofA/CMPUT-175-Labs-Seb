from bstack import BoundedStack, CHEMICAL_UNIT
from bqueue import BoundedQueue
import os

ANSI = {
    "RED": "\033[41m", # Red background
    "GREEN": "\033[42m", # Green background
    "YELLOW": "\033[43m", # Yellow background
    "ORANGE": "\033[48;5;202m", # Orange background
    "BLUE": "\033[44m", # Blue background
    "MEGENTA": "\033[45m", # Megenta background
    "RESET": "\033[0m" # Reset to default

}
    

def initialize_game_from_file(filename):
    with open(filename, 'r') as file:
        num_flasks, _ = map(int, file.readline().split())
        flasks = [BoundedStack() for _ in range(num_flasks)]
        chemical_queue = BoundedQueue(capacity=4)

        for line in file:
            line = line.strip()
            if 'F' in line:
                quantity, flask_index = map(int, line.split('F'))
                for _ in range(quantity):
                    if not chemical_queue.is_empty():
                        chemical = chemical_queue.dequeue()
                        flasks[flask_index - 1].initialize_stack(chemical)
            else:
                chemical_queue.enqueue(line)

    return flasks




def pour_chemical(source, destination, flasks):
    if source == destination:
        print("Cannot pour into the same flask. Try again.")
        return False
    if flasks[source].is_empty() or flasks[source].is_sealed():
        print("Cannot pour from that flask. Try again.")
        return False
    if flasks[destination].is_full() or flasks[destination].is_sealed():
        print("Cannot pour into that flask. Try again.")
        return False
    
    try:
        chemical = flasks[source].pop()
        flasks[destination].push(chemical)
        if flasks[destination].size() >= CHEMICAL_UNIT:
            # After pouring, we check if the last 3 items are the same and seal the flask
            if flasks[destination].is_sealed():
                # Your logic to seal the flask, if needed
                pass
        return True
    except Exception as e:
        print(e)
        return False




def display_flasks(flasks):
    flask_height = 4  # Maximum height for visual representation of flasks
    num_flasks = len(flasks)
    
    # Print the top caps for all flasks
    for flask in flasks:
        print("+--+" if flask.is_sealed() else "    ", end=" ")
    print()

    # Display the contents of each flask from bottom to top
    for layer in range(flask_height - 1, -1, -1):
        for flask in flasks:
            # Check if the current layer has a chemical or should be empty
            if layer < flask.size():
                colour = ANSI["RESET"]
                chemical = flask.get_item(layer)
                if chemical == "AA":
                    colour = ANSI["RED"]
                elif chemical == "BB":
                    colour = ANSI["BLUE"]                
                elif chemical == "CC":
                    colour = ANSI["GREEN"]
                elif chemical == "DD":
                    colour = ANSI["YELLOW"]
                elif chemical == "EE":
                    colour = ANSI["ORANGE"]
                elif chemical == "FF":
                    colour = ANSI["MEGENTA"]
                print(f"|{colour}{chemical}{ANSI['RESET']}|", end=" ")
            else:
                print("|  |", end=" ")
        print()

    # Print the bottom of the flasks
    for _ in range(num_flasks):
        print("+--+", end=" ")
    print()

    # Print the flask numbers aligned to the center below each flask
    for number in range(1, num_flasks + 1):
        print(f" {number:^3}", end=" ")  # Centered within a 3-char wide field
    print("\n")  # Extra newline for spacing


def clear_screen():
    print(ANSI["RESET"], end=' ') # reset to the default color
    os.system("")
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def get_valid_input(prompt, num_flasks):
    while True:
        user_input = input(prompt).strip()
        if user_input.lower() == 'exit':
            return 'exit'
        try:
            selected_index = int(user_input) - 1
            if 0 <= selected_index < num_flasks:
                return selected_index
            else:
                print("\033[1A\033[K", end='')  # Move cursor up and clear line
                print("Invalid selection. Please try again or type 'exit' to quit.")
                print("\033[1A\033[2K", end='')  # Move cursor up twice and clear line
        except ValueError:
            print("\033[1A\033[K", end='')  # Move cursor up and clear line
            print("Please enter a number or 'exit'.")
            print("\033[1A\033[2K", end='')  # Move cursor up twice and clear line

def main():
    filename = "chemicals.txt"  # Adjust as necessary
    flasks = initialize_game_from_file(filename)
    
    game_win_condition = False
    while not game_win_condition:
        display_flasks(flasks)
        source_index = get_valid_input("Select source flask: ", len(flasks))
        if source_index == 'exit':
            return  # Exit the function directly, ending the program

        destination_index = get_valid_input("Select destination flask: ", len(flasks))
        if destination_index == 'exit':
            return  # Exit the function directly, ending the program

        if not pour_chemical(source_index, destination_index, flasks):
            continue  # If pour is not successful, skip the rest of the loop and start over

        game_win_condition = all(flask.is_empty() or flask.is_sealed() for flask in flasks)
        if game_win_condition:
            display_flasks(flasks)
            print("You win!")

if __name__ == "__main__":
    main()


