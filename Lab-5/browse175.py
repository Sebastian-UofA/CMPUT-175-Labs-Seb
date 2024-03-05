import os
from time import sleep
import stack

#----------------------------------------------------
# Lab 5 Problem B: BROWSE-175
# Purpose of program:
#
# Author: Sebastian Perez
# Collaborators/references:
#----------------------------------------------------

os.system("")  # enables ANSI characters in terminal

def print_location(x, y, text):
    '''
    Prints text at the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
        - text (str): text to print
    Returns: N/A
    '''
    print ("\033[{1};{0}H{2}".format(x, y, text))

def clear_screen():
    '''
    Clears the terminal screen for future contents.
    Input: N/A
    Returns: N/A
    '''
    if os.name == "nt":  # windows
        os.system("cls")
    else:
        os.system("clear")  # unix (mac, linux, etc.)
        
def display_error(error):
    '''
    Displays an error message under the current site as specificed by "error".
    Input:
        - error (str): error message to display
    Returns: N/A
    '''
    move_cursor(0, 3)
    print("\033[6;31;40m{:^80}\033[0m".format(error))
    sleep(0.9)
    clear_screen()

def print_header():
    '''
    Prints the BROWSE-175 header.
    Input: N/A
    Returns: N/A 
    '''
    print("\033[0;32;40m{:^80}\033[0m".format("[ BROWSE-175 ]"))

def move_cursor(x, y):
    '''
    Moves the cursor to the specified location on the terminal.
    Input:
        - x (int): row number
        - y (int): column number
    Returns: N/A
    '''
    print("\033[{1};{0}H".format(x, y), end='')

def display_current_site(current):
    '''
    Displays the current site underneath the header.
    Input:
        - current (str): current site
    Returns: N/A
    '''
    print("\033[2;32;40m{:^80}\033[0m".format("Currently viewing: " + current))
    print("\033[4;30;40m{:^80}\033[0m".format(""))

def display_hint(message):
    '''
    Displays navigation hint message in the terminal.
    Input:
        - message (str): navigation hint message
    Returns: N/A
    '''
    print("\033[40;30;47m{:^80}\033[0m".format(message))

def display_buttons(back, fwd):
    '''
    Displays the navigational buttons at the top of the terminal.
    "(<) BACK" and "FORWARD (>)" labels should only be displayed
    if there are sites to go back or forward to.
    Input: 
        - back: stack of previous sites
        - fwd: stack of forward sites
    Returns: N/A
    '''
    if not back.isEmpty():  # If there are sites to go back to
        print("\033[1;37;40m{:<}\033[0m".format("(<) BACK"), end='')
    else:
        print("\033[1;37;40m{:<}\033[0m".format("        "), end='')

    if not fwd.isEmpty():  # If there are sites to go forward to
        print("\033[1;37;40m{:>72}\033[0m".format("FORWARD (>)"), end='')
    else:
        print("\033[1;37;40m{:>72}\033[0m".format(""), end='')
    

def goToNewSite(current, bck, fwd):
    '''
    Prompts the user for a new website address, updates the stacks, and returns the new address.
    Inputs:
        current: Current website address (str)
        bck: Reference to the Stack holding webpage addresses to go back to (Stack)
        fwd: Reference to the Stack holding webpage addresses to go forward to (Stack)
    Returns:
        new_current: New website address (str)
    '''
    # Prompt user for new site
    newsite = input('URL: ')
        
    # Eliminate all forward pages of the current page
    while not fwd.isEmpty():
        fwd.pop()
        
    # Add the new site to the back stack
    bck.push(current)
        
    # Update the current page
    new_current = newsite
        
    return new_current

def goBack(current, bck, fwd):
    '''
    This function is called when the user enters '<' during getAction(). It handles any exceptions that are raised by the Stack class 
    (i.e., when there are no webpages stored in the back history) by displaying an error message and returning the current site (str). 
    Otherwise, the previous webpage is retrieved (and returned as a string), and the two stacks are updated as appropriate.
    Inputs:
        current: Current website address (str)
        bck: Reference to the Stack holding webpage addresses to go back to (Stack)
        fwd: Reference to the Stack holding webpage addresses to go forward to (Stack)
    Returns:
        new_current: New website address (str) or current website address (str) if back stack is empty
    Raises:
        Exception: If there are no webpages stored in the back history
    '''
    # Check if the back stack is empty
    try:
        # Pop the top website from the back stack and assign it to new_current
        new_current = bck.pop()

        # Push the current website to the forward stack
        fwd.push(current)
        return new_current
    
    except Exception as e:
        print(e)
        display_error("Cannot go Back")
        return current

def goForward(current, bck, fwd):
    '''
    Moves the browser forward to the next webpage in the forward history.

    This function is called when the user enters '>' during getAction(). It handles any exceptions that are raised by the Stack class.

    Args:
        current (str): The current webpage.
        bck (Stack): The stack containing the back history of webpages.
        fwd (Stack): The stack containing the forward history of webpages.

    Returns:
        str: The new current webpage after moving forward.

    Raises:
        EmptyStackError: If there are no webpages stored in the forward history.
    '''    
    # Check if the forward stack is empty
    try:
        # Pop the top website from the forward stack and assign it to new_current
        new_current = fwd.pop()
        # Push the current website to the back stack
        bck.push(current)
        return new_current
    
    except Exception as e:
        print(e)
        display_error("Cannot go Forward")
        return current

def main():
    HOME = 'www.cs.ualberta.ca'
    back = stack.Stack()
    fwd = stack.Stack()
    current = HOME
    quit = False

    while not quit:
        clear_screen()
        print_header()
        display_current_site(current)

        # TODO: call display_buttons to show navigational buttons
        display_buttons(back, fwd)


        move_cursor(0, 20)
        display_hint("Use <, > to navigate, = to enter a URL, q to quit")
        print_location(5, 5, "Action: ")
        move_cursor(13, 5)
        action = input()
        if action == '=':
            current = goToNewSite(current, back, fwd)
        elif action == '<':
            current = goBack(current, back, fwd)
        elif action == '>':
            current = goForward(current, back, fwd)
        elif action == 'q':
            clear_screen()
            quit = True
        else:
            display_error('Invalid action!')
  

if __name__ == "__main__":
    main()