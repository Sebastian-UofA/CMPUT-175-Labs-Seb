import os 
import json
import time
from circular_dlinked_list import Node, CircularDoublyLinkedList
from art import Art


def clear_screen():
    '''
    clears the screen based on the operating system
    '''
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_json(filename):
    """
    Loads data from a JSON file.

    Parameters:
    - filepath (str): Path to the JSON file.

    Returns:
    - dict/list: Data loaded from the JSON file.
    """
    with open(filename, 'r', encoding='utf-8') as file:   #first takes a filename as input, opens the file, and loads its contents as JSON formatted string into a python dictionary
        data = json.load(file)
    return data 

def emoji_dict(json_data):
    '''
    Loads emoji data from a JSON file and creates a dictionary for lookup of emoji.

    Parameters:
    - filepath (str): The path to the JSON file containing emoji data.

    Returns:
    - dict: A dictionary where keys are emoji names (str) and values are emoji symbols (str).
    '''
    emoji_dict = {}
    for category in json_data:
        for name, character in category["emojis"].items():
            emoji_dict[name] = character
    return emoji_dict

def get_emoji(emoji_name, emoji_dict):
    '''
    Retrieves the symbol for a given emoji name from the emoji dictionary.
    Parameters:
    - emoji_name (str): The name of the emoji to look up.
    - emoji_data (dict): The dictionary containing emoji names as keys and their symbols as values.

    Returns:
    - str: The symbol of the emoji if found; otherwise, returns "Emoji not found."
    '''
    return emoji_dict.get(emoji_name, "Emoji not found")

def find_object(emoji_dict):
    '''
    Searches for and retrieves the emoji data by name.

    Parameters:
    - json_data (list): The loaded list of emoji data from JSON.
    - name (str): The name of the emoji to find.

    Returns:
    - dict: The emoji data if found; None otherwise.
    '''
    print('What do you want to add?')
    emoji_name = input().lower().strip()
    emoji = get_emoji(emoji_name, emoji_dict)
    
    if emoji == "Emoji not found":
        print(emoji)
        time.sleep(1)
        clear_screen()
        return None
    return emoji


def new_node(carousel, emoji_dict, carousel_capacity, art_frame):
    '''
    Adds a new node with the given data to the carousel.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel to which the node will be added.
    - data (str): The data to be stored in the new node.

    Returns:
    - None
    '''
    if carousel.get_size() >= carousel_capacity:
        print('You cannot add emojis! Carousel is Full. delete an emoji to add a new one.')
        time.sleep(2)
        clear_screen()
        return 

    emoji = find_object(emoji_dict)
    if emoji == None:
        return # emoji not found 
    if carousel.get_size() == 0:
        carousel.add_node(emoji)
        art_frame.initialization()
        
    elif carousel.get_size() == 1:
        new_pos = input('On which side do you want to add the emoji frame? (left/right)').lower()
        while new_pos not in ['left', 'right']:
            print('Invalid entry. Please enter left or right')
            new_pos = input('On which side do you want to add the emoji frame? (left/right)').lower()
            

        if new_pos == 'left':
            art_frame.add_left_from_one() #art stuff
            carousel.add_node_left(emoji)
            
        else:
            art_frame.add_right_from_one() #art stuff 
            carousel.add_node_right(emoji)
            
    else:
        new_pos = input('On which side do you want to add the emoji frame? (left/right): ').lower()
        while new_pos not in ['left', 'right']:
            print('Invalid entry. Please enter left or right')
            new_pos = input('On which side do you want to add the emoji frame? (left/right): ').lower()

        if new_pos == 'left':
            prev_emoji = carousel.head.get_prev().get_data()
            current_emoji = carousel.head.get_data()
            # pass the prev_emoji and current_emoji for left addition
            art_frame.add_left_from_multiple(prev_emoji, current_emoji) 
            carousel.add_node_left(emoji)
            
        else:
            prev_emoji = carousel.head.get_prev().get_data()
            current_emoji = carousel.head.get_data()
            # pass the prev_emoji and current_emoji for right addition
            art_frame.add_right_from_multiple(prev_emoji, current_emoji)
            carousel.add_node_right(emoji)
            

def delete_node(carousel, art_frame):
    '''
    Deletes the current node in the carousel.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel object.

    Returns:
    - None
    '''
    if carousel.get_size() == 0:
        print("The carousel is empty. There's nothing to delete.")
        return
    
    # Proceed with deletion
    carousel.delete_current_node()
    
    # Decide what to display based on the new size of the carousel
    if carousel.get_size() == 0:
        # The carousel is now empty
        print("All items have been deleted from the carousel.")
        time.sleep(2)
        clear_screen()
        # If you have a specific art frame for an empty carousel, display it here
    elif carousel.get_size() == 1:
        # Only one item left in the carousel
        art_frame.delete_from_one()  # Adjust based on method definition
    else:
        # More than one item remains in the carousel
        prev_emoji = carousel.head.get_prev().get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.delete_from_multiple(prev_emoji, next_emoji)

def display_info(carousel, json_data):
    '''
    Displays information about the current node in the carousel.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel containing the node.

    Returns:
    - None
    '''
    current_emoji = carousel.head.get_data()
    for category in json_data:
        if current_emoji in category["emojis"].values():
            print(f'Name: {list(category["emojis"].keys())[list(category["emojis"].values()).index(current_emoji)]}')
            print(f'Symbol: {current_emoji}')
            print(f'Category: {category["class"]}')
    time.sleep(1)
    input('Press ENTER to continue...')
    clear_screen()


def traverse_left(carousel, art_frame):
    '''
    Moves the current position in the carousel one node to the left.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel to traverse.

    Returns:
    - None
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving left
        carousel.move_prev()  # Move to the previous node first
        prev_emoji = carousel.head.get_prev().get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.move_left(prev_emoji, next_emoji)  # Pass the emojis to move_left()


def traverse_right(carousel, art_frame):
    '''
    Moves the current position in the carousel one node to the right.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel to traverse.

    Returns:
    - None
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving right
        carousel.move_next()  # Move to the next node first
        prev_emoji = carousel.head.get_prev().get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.move_right(prev_emoji, next_emoji)  # Pass the emojis to move_right()

def get_input(carousel):
    '''
    Prompts the user for an action command. checks if the input is valid.

    Returns:
    - str: The action command entered by the user.
    '''

    allowed_actions = ['L', 'R', 'ADD', 'DEL', 'INFO', 'Q']
    is_valid_input = False  # Flag to track if input is valid
    user_input = ""

    while not is_valid_input:
        if carousel.get_size() == 0:
            print('Type any of the following commands to perform the action:')
            print('    ADD: Add an emoji frame')
            print('    Q: Quit the program')
        elif carousel.get_size() == 1:
            print('Type any of the following commands to perform the action:')
            print('    ADD: Add an emoji frame')
            print('    DEL: Delete an emoji frame')
            print('    INFO: Retrieve info about the current frame')
            print('    Q: Quit the program')
        else:  # Assuming carousel.get_size() >= 2
            print('Type any of the following commands to perform the action:')
            print('    L: Move left')
            print('    R: Move right')
            print('    ADD: Add an emoji frame')
            print('    DEL: Delete an emoji frame')
            print('    INFO: Retrieve info about the current frame')
            print('    Q: Quit the program')
        user_input = input('>> ').upper().strip()


        if user_input in allowed_actions:
            is_valid_input = True  # Set flag to true when valid input is received
        else:
            print("Invalid entry. Please enter a valid command.")
            time.sleep(1)
            clear_screen()  # Clear the screen and prompt again
            return None
        

    return user_input


def carousel_display(carousel, art_frame):
    '''
    Displays the entire carousel, highlighting the current node.

    Parameters:
    - carousel (CircularDoublyLinkedList): The carousel to display.

    Returns:
    - None
    '''

    if carousel.get_size() == 0:
        # nothing displayed
        art_frame.initialization()
    elif carousel.get_size() == 1:
        # Display carousel with one item
        current_emoji = carousel.get_current_node().get_data()
        art_frame.display_one_item(current_emoji)
    else:
        # For carousel with multiple items
        prev_emoji = carousel.head.get_prev().get_data()
        current_emoji = carousel.head.get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.display_multiple_items(prev_emoji, current_emoji, next_emoji)



def main():
    '''
    main function to run the program, includes the main loop for the carousel program
    '''
    emojis_data_file = load_json("emojis.json") 
    emojis_dict = emoji_dict(emojis_data_file) 
    art_frame = Art()
    carousel_capacity = 5
    carousel = CircularDoublyLinkedList(carousel_capacity)
    quit_program = False  

    while not quit_program:
        if carousel.get_size() == 0:
            action = get_input(carousel)
            
        else:
            carousel_display(carousel, art_frame)
            action = get_input(carousel)
            

        try:
            if action == 'ADD':
                new_node(carousel, emojis_dict, carousel_capacity, art_frame)
            elif action == 'L' and carousel.get_size() > 0:
                traverse_left(carousel, art_frame)
            elif action == 'R' and carousel.get_size() > 0:
                traverse_right(carousel, art_frame)
            elif action == 'DEL' and carousel.get_size() > 0:
                delete_node(carousel, art_frame)  
            elif action == 'INFO' and carousel.get_size() > 0:
                display_info(carousel, emojis_data_file)
            elif action == 'Q':
                quit_program = True  # Set the flag to True to exit the loop
        except Exception as e:
            carousel_display(carousel, art_frame)  # Display the carousel again
            print(e)

if __name__ == "__main__":
    main()