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
    

def create_queues_from_file(filename):
    with open(filename, 'r') as file:
        # First line contains the number of flasks; ignoring chemicals count as it's not used directly
        num_flasks, _ = map(int, file.readline().split())
        flasks = [BoundedStack(capacity=4) for _ in range(num_flasks)] # creates a list of bounded stacks for flasks
        chemical_queue = BoundedQueue(capacity=4) # creates a bounded queue for chemicals

        for line in file:
            line = line.strip()
            if line[-1].isdigit() and 'F' in line: 
                # When the line specifies chemicals to be added to a flask
                amount, flask_index = map(int, line.split('F'))
                for _ in range(amount):
                    if not chemical_queue.is_empty():
                        chemical = chemical_queue.dequeue()
                        flasks[flask_index - 1].push(chemical)
            else:
                # Otherwise, enqueue the chemical into the queue
                if not chemical_queue.is_full():
                    chemical_queue.enqueue(line)

    return flasks


def transfer_chemical(source, destination, flasks):
    if source == destination:
        return False, "Cannot pour into the same flask. Try again."
    if flasks[source].is_empty() or flasks[source].is_sealed():
        return False, "Cannot pour from that flask. Try again."
    if flasks[destination].is_full() or flasks[destination].is_sealed():
        return False, "Cannot pour into that flask. Try again."
    
    try:
        chemical = flasks[source].pop()
        flasks[destination].push(chemical)
        if flasks[destination].size() >= CHEMICAL_UNIT and not flasks[destination].is_sealed():
            # seal the flask if needed
            pass
        return True, None
    except Exception as e:
        return False, str(e)


def print_flasks(flasks, source_prompt="", destination_prompt=""):
    clear_screen()  # Clear the screen 
    print("Magical Flask Game\n")
    
    if source_prompt:
        print(f"Select source flask: {source_prompt}")
    else:
        print("Select source flask: ")
    
    if destination_prompt:
        print(f"Select destination flask: {destination_prompt}")
    else:
        print("Select destination flask: ")

    flask_height = 4  # Maximum height of flasks
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
        print(f" {number:^3}", end=" ")  
    print("\n")  


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
            # After displaying the error, reposition the cursor back to the input position.
            print(f"\033[{line_number};{len(prompt)}H", end='')


def main():
    filename = "chemicals.txt"  
    flasks = create_queues_from_file(filename)
    
    game_win_condition = False
    while not game_win_condition:
        print_flasks(flasks)
        
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
            if transfer_chemical(source_index, destination_index, flasks):
                print("Chemical transfered.")
            else:
                display_error_message("Invalid Input. Try Again")
        except ValueError:
            display_error_message("Invalid Input. Try Again")

        game_win_condition = all(flask.is_empty() or flask.is_sealed() for flask in flasks)
        if game_win_condition:
            print_flasks(flasks)
            print("You win!")

if __name__ == "__main__":
    main()

# works inside vscode IDE and os terminal with some quirks
# displays error message very breifly when trying to pour chemical from a sealed flask
# terminal closes after the game is won, so the win message is not visible