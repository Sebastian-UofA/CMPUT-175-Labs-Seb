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
        return False, "Cannot pour into the same flask. Try again."
    if flasks[source].is_empty() or flasks[source].is_sealed():
        return False, "Cannot pour from that flask. Try again."
    if flasks[destination].is_full() or flasks[destination].is_sealed():
        return False, "Cannot pour into that flask. Try again."
    
    try:
        chemical = flasks[source].pop()
        flasks[destination].push(chemical)
        return True, ""
    except Exception as e:
        return False, str(e)





def display_flasks(flasks, source_prompt="", destination_prompt=""):
    clear_screen()  # Clear the screen for a fresh display
    print("Magical Flask Game\n")
    
    if source_prompt:
        print(f"Select source flask: {source_prompt}")
    else:
        print("Select source flask: ")
    
    if destination_prompt:
        print(f"Select destination flask: {destination_prompt}")
    else:
        print("Select destination flask: ")

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

def display_error_message(message):
    # Move the cursor to line 5 and print the error message
    print("\033[5;0H\033[2K" + message, end='', flush=True)

def clear_error_message():
    # Clear the error message from line 5
    print("\033[5;0H\033[2K", end='', flush=True)

def request_input(prompt, line_number, valid_values=None):
    while True:
        # Move the cursor to the prompt line and clear it
        print(f"\033[{line_number};0H\033[2K", end='', flush=True)  # Move to line, clear line
        print(prompt, end='', flush=True)
        user_input = input()
        if valid_values is None or user_input in valid_values:
            clear_error_message()
            return user_input
        else:
            display_error_message("Invalid Input. Try Again")
            # After displaying the error, we need to reposition the cursor back to the input position.
            print(f"\033[{line_number};{len(prompt)}H", end='')


def main():
    filename = "chemicals.txt"  # Example filename, adjust as necessary
    flasks = initialize_game_from_file(filename)
    
    game_win_condition = False
    while not game_win_condition:
        display_flasks(flasks)
        
        # Request source flask input
        source = request_input("Select source flask: ", 3, valid_values=[str(i) for i in range(1, len(flasks)+1)] + ['exit'])
        if source.lower() == 'exit':
            return
        
        # Request destination flask input
        destination = request_input("Select destination flask: ", 4, valid_values=[str(i) for i in range(1, len(flasks)+1)] + ['exit'])
        if destination.lower() == 'exit':
            return

    try:
        source_index = int(source) - 1
        destination_index = int(destination) - 1

        # Attempt to pour the chemical and get the result and any error message
        success, error_message = pour_chemical(source_index, destination_index, flasks)

        if success:
            # If successful, ensure any previous error message is cleared
            clear_error_message()
            print("Chemical poured successfully.")
        else:
            # If there was an error, display it
            # No need to clear the error here, as display_error_message() will overwrite it
            display_error_message(error_message)
            
    except ValueError:
        # This is triggered if source or destination indexes are not integers,
        # which should not happen due to earlier input validation
        display_error_message("Invalid Input. Try Again")


        game_win_condition = all(flask.is_empty() or flask.is_sealed() for flask in flasks)
        if game_win_condition:
            display_flasks(flasks)
            print("You win!")

if __name__ == "__main__":
    main()

