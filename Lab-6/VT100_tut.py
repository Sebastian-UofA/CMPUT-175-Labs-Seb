import os

# ANSI escape codes dictionary for setting text and background colors, underlining text, and resetting formatting.
ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "HRED": "\033[41m",  # Background Red
    "HGREEN": "\033[42m",  # Background Green
    "HBLUE": "\033[44m",  # Background Blue
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
    "CLEARLINE": "\033[0K"
}

# Clears the terminal screen based on the operating system executing the script.
def clear_screen():
    print(ANSI["RESET"], end='')  # Resets any ongoing text styling to default.
    if os.name == "nt":  # Windows
        os.system("cls")
    else:  # MacOS_etc
        os.system("clear")

# Moves the cursor to a specified position (x, y) on the terminal.
def move_cursor(x, y):
    print(f"\033[{y};{x}H", end='', flush=True)

# Clears the content from the cursor's current position to the end of the line.
def clear_line():
    print(ANSI["CLEARLINE"], end='', flush=True)
    

# Prints the title "VT100 SIMULATOR" with specified text and background colors.
def print_title(text_color, bg_color):
    bg_style = "" if bg_color == "NONE" else ANSI["H" + bg_color]  # Checks if background color is set to "NONE".
    # Constructs the title text with the specified styles.
    title_text = ANSI["UNDERLINE"] + ANSI[text_color] + bg_style + "VT100 SIMULATOR" + ANSI["RESET"]
    clear_screen()  # Clears screen to update the title at the same position every time the function is called.
    print(title_text)

# Prints a prompt at a specified position and takes user input, ensuring it's one of the valid inputs provided.
def take_input(prompt, x, y, valid_inputs):
    move_cursor(x, y)  # Moves cursor to specified coordinates for input.
    clear_line()  # Clears any previous input line.
    print(prompt, end='', flush=True)
    while True:
        user_input = input().strip().upper()  # Captures and processes user input.
        if user_input in valid_inputs:  # Checks if the input is valid.
            return user_input
        else:  # If input is invalid, it prompts the user again.
            move_cursor(x, y)
            clear_line()
            print(prompt, end='', flush=True)

# Initial setup: Enable ANSI escape codes support and clear the screen.
os.system("") 
clear_screen()

# Prints the initial title with default "BLUE" text color and no background color.
print_title("BLUE", "NONE")

# Main loop which repeatedly asks for text and background color until "EXIT" is entered.
while True:
    # Asks for text color input. Positioning on x=0, y=3 ensures it's placed below the title.
    text_color = take_input("Enter a text colour: ", 0, 3, ["RED", "GREEN", "BLUE", "EXIT"])
    if text_color == "EXIT":  # Exit condition.
        break

    # Asks for background color input. Positioned right below the text color input.
    bg_color = take_input("Enter a background colour: ", 0, 4, ["RED", "GREEN", "BLUE", "NONE", "EXIT"])
    if bg_color == "EXIT":  # Exit condition.
        break

    # Re-prints the title with the new colors selected by the user.
    print_title(text_color, bg_color)

# Resets terminal formatting to default after exiting the loop.
print(ANSI["RESET"])
