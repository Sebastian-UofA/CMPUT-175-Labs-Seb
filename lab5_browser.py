#----------------------------------------------------
# Lab 5, Exercise 2: Web browser simulator
# Purpose of program: Simulate a web browser using stacks to store the back and forward history of webpages.
#
# Author: Sebastian Perez
# Collaborators/references:
#----------------------------------------------------

from stack import Stack

def getAction():
    '''
    Asks the user for an action input and validates the input. Otherwise raises an exception displaying an error message.
    Inputs: None
    Returns: Valid character entered by the user (str)
    '''
    
    allowed_action =  ['=', '<', '>', 'q']

    user_input = input('Enter = to enter a URL, < to go back, > to go forward, or q to quit: ').strip()
    while user_input not in allowed_action:
        raise Exception('Invalid entry. Please enter =, <, >, or q: ')
    return user_input


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
        
    # Eliminate all forward pages of the current page (loop continues until the fwd stack is empty)
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
        print("Cannnot go back.")
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
        print("Cannot go forward.")
        return current

def main():
    '''
    Controls main flow of web browser simulator
    Inputs: N/A
    Returns: None
    '''    
    HOME = 'www.cs.ualberta.ca'
    back = Stack()
    forward = Stack()
    
    current = HOME
    quit = False
    
    while not quit:
        print('\nCurrently viewing', current)
        try:
            action = getAction()
            
        except Exception as actionException:
            print(actionException.args[0])
            
        else:
            if action == '=':
                current = goToNewSite(current, back, forward)
            #TO DO: add code for the other valid actions ('<', '>', 'q')
            #HINT: LOOK AT LAB 4
            elif action == '<':
                current = goBack(current, back, forward)
            elif action == '>':
                current = goForward(current, back, forward)
            elif action == 'q':
                quit = True
            
    print('Browser closing...goodbye.')    

        
if __name__ == "__main__":
    main()
    