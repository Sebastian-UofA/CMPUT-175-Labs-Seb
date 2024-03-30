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
    emoji_dict = {}
    for category in json_data:
        for name, character in category["emojis"].items():
            emoji_dict[name] = character
    return emoji_dict

def get_emoji(emoji_name, emoji_dict):
    return emoji_dict.get(emoji_name, "Emoji not found")


def new_node(carousel, emoji_dict, carousel_capacity, art_frame):
    '''
    A function that handles adding new nodes into the circular doubly-linked list. 
    '''
    if carousel.get_size() >= carousel_capacity:
        print('The carousel is at full capacity. Please delete a frame before adding a new one.')
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
            prev_emoji = carousel.head.get_prev().get_data() if carousel.head.get_prev() else " "
            current_emoji = carousel.head.get_data()
            # Only pass the prev_emoji and current_emoji for left addition
            art_frame.add_left_from_multiple(prev_emoji, current_emoji)  # Assuming similar pattern for left addition
            carousel.add_node_left(emoji)
            
        else:
            prev_emoji = carousel.head.get_prev().get_data() if carousel.head.get_prev() else " "
            current_emoji = carousel.head.get_data()
            # Only pass the prev_emoji and current_emoji for right addition
            art_frame.add_right_from_multiple(prev_emoji, current_emoji)
            carousel.add_node_right(emoji)
            

def delete_node():
    '''
    A function that handles deleting nodes from the circular doubly-linked list. 
    '''
    pass

def find_object(emoji_dict):
    '''
    A function to find the object to be added to the circular doubly-linked list.  
    '''
    print('What do you want to add?')
    emoji_name = input()
    emoji = get_emoji(emoji_name, emoji_dict)
    if emoji == "Emoji not found":
        print(emoji)
        return None
    return emoji

def traverse_left(carousel, art_frame):
    '''
    A function that handles traversing left in the circular doubly-linked list. 
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving left
        carousel.move_prev()  # Move to the previous node first
        prev_emoji = carousel.head.get_prev().get_data() if carousel.head.get_prev() else " "
        next_emoji = carousel.head.get_next().get_data() if carousel.head.get_next() else " "
        art_frame.move_left(prev_emoji, next_emoji)  # Pass the emojis to move_left()


def traverse_right(carousel, art_frame):
    '''
    A function that handles traversing right in the circular doubly-linked list. 
    '''
    if carousel.get_size() > 0:
        # Get the emojis for the nodes before and after moving right
        carousel.move_next()  # Move to the next node first
        prev_emoji = carousel.head.get_prev().get_data() if carousel.head.get_prev() else " "
        next_emoji = carousel.head.get_next().get_data() if carousel.head.get_next() else " "
        art_frame.move_right(prev_emoji, next_emoji)  # Pass the emojis to move_right()

def get_input(carousel):
    allowed_actions = ['L', 'R', 'ADD', 'DEL', 'INFO', 'Q']
    is_valid_input = False  # Flag to track if input is valid
    user_input = ""

    while not is_valid_input:
        if carousel.get_size() == 0:
            print('Type any of the following commands to perform the action:')
            print('ADD: Add an emoji frame')
            print('Q: Quit the program')
        elif carousel.get_size() == 1:
            print('Type any of the following commands to perform the action:')
            print('ADD: Add an emoji frame')
            print('DEL: Delete an emoji frame')
            print('INFO: Retrieve info about the current frame')
            print('Q: Quit the program')
        else:  # Assuming carousel.get_size() >= 2
            print('Type any of the following commands to perform the action:')
            print('L: Move left')
            print('R: Move right')
            print('ADD: Add an emoji frame')
            print('DEL: Delete an emoji frame')
            print('INFO: Retrieve info about the current frame')
            print('Q: Quit the program')
        user_input = input().upper()

        if user_input in allowed_actions:
            is_valid_input = True  # Set flag to true when valid input is received
        else:
            print("Invalid entry. Please enter a valid command.")
            time.sleep(1)
            clear_screen()  # Clear the screen and prompt again

    return user_input


# Within the carousel_display function in carousel.py
def carousel_display(carousel, art_frame):
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
    emojis_dict = emoji_dict(emojis_data_file)  # Make sure to use a different name to not shadow the function
    art_frame = Art()
    carousel_capacity = 5
    carousel = CircularDoublyLinkedList(carousel_capacity)
    quit_program = False  

    while not quit_program:
        # Only get input if the carousel is empty
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
                delete_node(carousel, art_frame)  # Make sure this function is implemented
            elif action == 'INFO' and carousel.get_size() > 0:
                # Logic to show info about the current node
                pass
            elif action == 'Q':
                quit_program = True  # Set the flag to True to exit the loop
        except Exception as e:
            print(e)

# Run the main function if this file is the entry point
if __name__ == "__main__":
    main()