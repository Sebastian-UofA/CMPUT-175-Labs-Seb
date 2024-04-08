import os
import time

class Art:
    def __init__(self):
        self.art_pieces = [
"""
                             ↓↓
 __________    |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|    __________
           |   |                            |   |          
           |   |                            |   |          
 <>        |   |             ()             |   |        ,.
           |   |                            |   |          
 __________|   |                            |   |__________
               |____________________________|
"""
,
"""
                             ↓↓
               |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|    
               |                            |          
               |                            |        
               |             ()             |       
               |                            |         
               |                            |  
               |____________________________|                            
"""
,
"""
                             /\\ 
 __________    |‾‾‾‾‾‾‾‾‾‾‾‾/  \\‾‾‾‾‾‾‾‾‾‾‾‾|    __________
           |   |           /    \\           |   |                   
           |   |          /_    _\\          |   |                   
 <>        |   |            |  |            |   |        ()        
           |   |            |  |            |   |                  
 __________|   |            |  |            |   |__________
               |____________|  |____________|
                            |__|
"""
,
"""
                             /\\ 
               |‾‾‾‾‾‾‾‾‾‾‾‾/  \\‾‾‾‾‾‾‾‾‾‾‾‾|   
               |           /    \\           |                    
               |          /_    _\\          |           
               |            |  |            |       
               |            |  |            |                  
               |            |  |            |   
               |____________|  |____________|
                            |__|                             
"""
,
"""
                                         |\\
 __________    |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| \\     __________
           |   |                         |  \\   |                   
           | |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    \\  |                   
 <>        | |            Right               | |        ()        
           | |___________________________    /  |                  
 __________|   |                         |  /   |__________
               |_________________________| /
                                         |/
"""
,
"""
                                         |\\
 __________    |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| \\     __________
           |   |                         |  \\   |                   
           | |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    \\  |                   
 <>        | |        Adding Right            | |        ()        
           | |___________________________    /  |                  
 __________|   |                         |  /   |__________
               |_________________________| /
                                         |/                             
"""
,
"""
                                         |\\
               |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| \\  
               |                         |  \\          
             |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾    \\          
             |        Adding Right            |    
             |___________________________    /    
               |                         |  /  
               |_________________________| /
                                         |/                             
"""
,
"""
                 /|                      
 __________     / |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|    __________
           |   /  |                         |   |                   
           |  /    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| |                   
 <>        | |              Left              | |        ()        
           |  \\    ___________________________| |                  
 __________|   \\  |                         |   |__________
                \\ |_________________________|
                 \\|                      
""" 
,
"""
                 /|                      
 __________     / |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|    __________
           |   /  |                         |   |                   
           |  /    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾| |                   
 <>        | |           Adding Left          | |        ()        
           |  \\    ___________________________| |                  
 __________|   \\  |                         |   |__________
                \\ |_________________________|
                 \\|                                                   
"""
,
"""
                 /|                      
                / |‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|   
               /  |                         |          
              /    ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾|      
             |           Adding Left          |       
              \\    ___________________________|             
               \\  |                         |   
                \\ |_________________________|
                 \\|                                                   
"""
,
"""
                            |‾‾|
               |‾‾‾‾‾‾‾‾‾‾‾‾|  |‾‾‾‾‾‾‾‾‾‾‾‾|   
               |            |  |            |                   
               |            |  |            |                    
               |           _|  |_           |   
               |          \\      /          |                
               |           \\    /           |   
               |____________\\  /____________|
                             \\/                            
"""]


    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def display_multiple_items(self, prev_emoji, current_emoji, next_emoji):
        # art frame string has placeholders for previous, current, and next emojis
        # For example: "<>  ()  ,."
        frame = self.art_pieces[0]
        frame = frame.replace("<>", prev_emoji).replace("()", current_emoji).replace(",.", next_emoji)
        print(frame)
        time.sleep(1)


    def display_one_item(self, current_emoji):
        frame = self.art_pieces[1]
        frame = frame.replace("()", current_emoji)
        print(frame)
        time.sleep(1)

    def delete_from_multiple(self, prev_emoji, next_emoji):
        self.clear_screen()
        frame = self.art_pieces[2]
        frame = frame.replace("<>", prev_emoji).replace("()", next_emoji)
        print(frame)
        time.sleep(1)
        self.clear_screen()

    def delete_from_one(self):
        self.clear_screen()
        print(self.art_pieces[3])
        time.sleep(1)
        self.clear_screen()

    def move_right(self, prev_emoji, next_emoji):
        self.clear_screen()
        frame = self.art_pieces[4]
        frame = frame.replace("<>", prev_emoji).replace("()", next_emoji)
        print(frame)
        time.sleep(1)
        self.clear_screen()

    def add_right_from_multiple(self, prev_emoji, next_emoji):
        self.clear_screen()
        frame = self.art_pieces[5]
        frame = frame.replace("<>", next_emoji).replace("()", prev_emoji) #
        print(frame)
        time.sleep(1)
        self.clear_screen()

    def add_right_from_one(self):
        self.clear_screen()
        print(self.art_pieces[6])
        time.sleep(1)
        self.clear_screen()

    def move_left(self, prev_emoji, next_emoji):
        self.clear_screen()
        frame = self.art_pieces[7]
        frame = frame.replace("<>", prev_emoji).replace("()", next_emoji)
        print(frame)
        time.sleep(1)
        self.clear_screen()

    def add_left_from_multiple(self, prev_emoji, next_emoji):
        self.clear_screen()
        frame = self.art_pieces[8]
        frame = frame.replace("<>", prev_emoji).replace("()", next_emoji)
        print(frame)
        time.sleep(1)
        self.clear_screen()

    def add_left_from_one(self):
        self.clear_screen()
        print(self.art_pieces[9])
        time.sleep(1)
        self.clear_screen()

    def initialization(self):
        self.clear_screen()
        print(self.art_pieces[10])
        time.sleep(1)
        self.clear_screen()



    
    