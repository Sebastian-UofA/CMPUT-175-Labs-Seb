#----------------------------------------------------
# Lab 4: Web browser simulator
# Purpose of program:
#
# Author: 
# Collaborators/references:
#----------------------------------------------------

def getAction():
    '''
    Write docstring to describe function
    Inputs: None
    Returns: Valid character entered by the user (str)
    '''
    # TO DO: delete pass and write your code here
    
    allowed_action =  ['=', '<', '>', 'q']
    while True:
        user_input = input('Enter = to go to a new site, < to go back, > to go forward, or q to quit: ')
        if user_input in allowed_action:
            return user_input
        else:
            user_input = input('Invalid input. Please enter =, <, >, or q: ')


def goToNewSite(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''   
    # TO DO: delete pass and write your code here
    new_site = input("URL: ")
    pages = pages[:current + 1]  # Remove forward history
    pages.append(new_site)  # Add new site to the end
    return len(pages) - 1  # Return the index of the new site
    
def goBack(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''    
    # TO DO: delete pass and write your code here
    if current == 0:
        print("Cannot go back.")
        return current
    else:
        return current - 1


def goForward(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''    
    # TO DO: delete pass and write your code here
    if current == len(pages) - 1:
        print("Cannot go forward.")
        return current
    else:
        return current + 1


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
    