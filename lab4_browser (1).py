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
    Inputs: ?
    Returns: ?
    '''
    # TO DO: delete pass and write your code here
    pass


def goToNewSite(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''   
    # TO DO: delete pass and write your code here
    pass

    
def goBack(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''    
    # TO DO: delete pass and write your code here
    pass


def goForward(current, pages):
    '''
    Write docstring to describe function
    Inputs: ?
    Returns: ?
    '''    
    # TO DO: delete pass and write your code here
    pass


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
    