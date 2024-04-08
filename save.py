import os 
import json
import time
from circular_dlinked_list import Node, CircularDoublyLinkedList
from art import Art


def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def load_json(filename):
    """
    Load JSON from a file
    """
    with open(filename, 'r', encoding='utf-8') as file:   #first takes a filename as input, opens the file, and loads its contents as JSON formatted string into a python dictionary
        data = json.load(file)
    return data 

def emoji_dict(json_data):
    """
    Loads emoji data from a JSON file and creates a dictionary for easy lookup.

    This function reads a JSON file containing emoji information and converts it into
    a dictionary structure where each key is an emoji name, and its value is the corresponding
    emoji symbol. The function is designed to facilitate quick access to emoji symbols
    based on their names.

    Parameters:
    - filepath (str): The path to the JSON file containing emoji data.

    Returns:
    - dict: A dictionary where keys are emoji names (str) and values are emoji symbols (str).
    """
    emoji_dict = {}
    for category in json_data:
        for name, character in category["emojis"].items():
            emoji_dict[name] = character
    return emoji_dict

def get_emoji(emoji_name, emoji_data):
    """
    Retrieves the symbol for a given emoji name from the emoji data. If the exact name
    isn't found, it suggests the closest match using the Levenshtein distance.

    Parameters:
    - emoji_name (str): The name of the emoji to look up.
    - emoji_data (dict): The dictionary containing emoji information.

    Returns:
    - str: The symbol of the emoji if found or confirmed by the user; 
           otherwise, indicates that the emoji wasn't found.
    """

    # Try to find an exact match first
    for category in emoji_data:
        if emoji_name in category["emojis"]:
            return category["emojis"][emoji_name]

    # If no exact match, find the closest match
    closest_name, _ = find_closest_emoji(emoji_name, emoji_data)
    if closest_name:
        confirmation = input(f"Did you mean '{closest_name}'? (Y/N): ").strip().lower()
        if confirmation == 'y':
            for category in emoji_data:
                if closest_name in category["emojis"]:
                    return category["emojis"][closest_name]
        else:
            return "Operation cancelled by user."
    return "Emoji not found."


def find_object(emoji_dict):
    '''
    A function to find the object to be added to the circular doubly-linked list.  
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

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def find_closest_emoji(input_name, emoji_data):
    closest_name = None
    min_distance = float('inf')
    
    for category in emoji_data:
        for emoji_name in category['emojis']:
            distance = levenshtein_distance(input_name, emoji_name)
            if distance < min_distance:
                min_distance = distance
                closest_name = emoji_name
                
    return closest_name, min_distance


def new_node(carousel, emoji_dict, carousel_capacity, art_frame):
    '''
    A function that handles adding new nodes into the circular doubly-linked list. 
    '''
    if carousel.get_size() >= carousel_capacity:
        print('The carousel is at full capacity. Please delete a frame before adding a new one.')
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
            # Only pass the prev_emoji and current_emoji for left addition
            art_frame.add_left_from_multiple(prev_emoji, current_emoji)  # Assuming similar pattern for left addition
            carousel.add_node_left(emoji)
            
        else:
            prev_emoji = carousel.head.get_prev().get_data()
            current_emoji = carousel.head.get_data()
            # Only pass the prev_emoji and current_emoji for right addition
            art_frame.add_right_from_multiple(prev_emoji, current_emoji)
            carousel.add_node_right(emoji)
            

def delete_node(carousel, art_frame):
    '''
    A function that handles deleting nodes from the circular doubly-linked list.
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
    A function that displays information about the current node in the circular doubly-linked list.
    '''
    current_emoji = carousel.head.get_data()
    for category in json_data:
        if current_emoji in category["emojis"].values():
            print(f'Name: {list(category["emojis"].keys())[list(category["emojis"].values()).index(current_emoji)]}')
            print(f'Symbol: {current_emoji}')
            print(f'Category: {category["class"]}')
    input('Press ENTER to continue...')
    clear_screen()


def traverse_left(carousel, art_frame):
    '''
    A function that handles traversing left in the circular doubly-linked list. 
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving left
        carousel.move_prev()  # Move to the previous node first
        prev_emoji = carousel.head.get_prev().get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.move_left(prev_emoji, next_emoji)  # Pass the emojis to move_left()


def traverse_right(carousel, art_frame):
    '''
    A function that handles traversing right in the circular doubly-linked list. 
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving right
        carousel.move_next()  # Move to the next node first
        prev_emoji = carousel.head.get_prev().get_data()
        next_emoji = carousel.head.get_next().get_data()
        art_frame.move_right(prev_emoji, next_emoji)  # Pass the emojis to move_right()

def get_input(carousel):
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
        user_input = input().upper()


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
    A function that displays the carousel and all the items within it at all times.
    '''

    if carousel.get_size() == 0:
        # Display an empty carousel or a welcome message
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