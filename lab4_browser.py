#----------------------------------------------------
# Lab 4: Web browser simulator
# Purpose of program:
#
# Author: 
# Collaborators/references:
#----------------------------------------------------

def getAction():
    '''
    Asks the user for an action input and validates the input. Otherwise keeps giving error message until a valid input is entered.
    Inputs: None
    Returns: Valid character entered by the user (str)
    '''
    
    allowed_action =  ['=', '<', '>', 'q']

    user_input = input('Enter = to enter a URL, < to go back, > to go forward, or q to quit: ').strip()
    while user_input not in allowed_action:
        user_input = input('Invalid entry. Please enter =, <, >, or q: ').strip()
    return user_input

def goToNewSite(current, pages):
    '''
    Asks the user to enter a new website, adds this website to the list of pages and the current index.
    Inputs: current (int) - the index of the current site, pages (list) - the list of websites
    Returns: current (int) - the updated index of the current site
    '''
    newSite = input('URL: ') # Ask the user to enter a new website
    # Append the new website to the list of pages
    pages.append(newSite)
    # Update the current index to point to the newly added website
    current = len(pages) - 1  # index of the last element in the list = CURRENT 
    return current
    
def goBack(current, pages):
    '''
    Goes back to the previous webpage if there are any webpages stored in websites list behind the current index.
    Inputs: current (int) - the index of the current site, pages (list) - the list of websites
    Returns: current (int) - the updated index of the current site
    '''
    if current > 0:
        # If the current index is greater than 0, return the previous index
        return current -1
    else:
        # Esle, display an error message
        print('Cannot go back.')
    return current

def goForward(current, pages):
    '''
    Goes forward to the next webpage if there are any webpages stored ahead of the current index in the websites list.
    Inputs: current (int) - the index of the current site, pages (list) - the list of websites
    Returns: current (int) - the updated index of the current site
    '''
    if current < len(pages) - 1: 
        # if current less than the last index, return the next index forward
        return current + 1
    else:
        # Else, display an error message
        print('Cannot go forward.')
    return current


def main():
    '''
    Controls main flow of web browser simulator
    Inputs: N/A
    Returns: None
    '''    
    HOME = 'www.cs.ualberta.ca'
    websites = [HOME]
    currentIndex = 0
    quit = False
    
    while not quit:
        print('\nCurrently viewing', websites[currentIndex])
        action = getAction()
        
        if action == '=':
            currentIndex = goToNewSite(currentIndex, websites)
        elif action == '<':
            currentIndex = goBack(currentIndex, websites)
        elif action == '>':
            currentIndex = goForward(currentIndex, websites)
        elif action == 'q':
            quit = True
    
    print('Browser closing...goodbye.')    

        
if __name__ == "__main__":
    main()
    