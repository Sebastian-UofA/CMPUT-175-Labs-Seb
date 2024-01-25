def getInputFile():
    """
    Ask the user for a file name, check if it ends with '.txt', and return it. If the file name is invalid, ask again (Resets the function).
    Returns:
    str: The name of the text file.
    """
    filename = input('Enter the input filename: ')
    if filename.endswith('.txt'):
        return filename
    else:
        print('Invalid filename extension. Please re-enter the input filename.')
        return getInputFile()


def decrypt(filename):
    """
    Decrypts the message from the provided text file using the Caesar cipher.

    Parameters:
    filename (str): The name of the text file.

    Returns:
    str: The decrypted message in lowercase.
    """
    with open(filename, 'r') as file:
        # Read and strip leading/trailing whitespace from both lines
        shift = int(file.readline().strip()) #reads line 1
        encrypted_message = file.readline().strip() #reads line 2 and stores it as a string

    decrypted_words = [] # Create an empty list to store the decrypted words
    for words in encrypted_message.split(): # Splits words separated by spaces into a list
        decrypted_word = "" #stores words 
        for letters in words:
            if letters.isalpha():
                # Decrypt the letter using the cipher key
                decrypted_letter = chr((ord(letters.lower()) - ord('a') - shift) % 26 + ord('a')) # ord() returns the ASCII value of a character and is subtracted by ord('a') to get alphabet position then subtracted by shift value
                decrypted_word += decrypted_letter  #add new letters to empty string              # % 26 is used to wrap around the alphabet and ord('a') is added to get the ASCII value of the decrypted character
        decrypted_words.append(decrypted_word) #add decrypted words to list

    decrypted_message = " ".join(decrypted_words) #join words in list with spaces
    return decrypted_message

def main():
    # help(getInputFile)
    # help(decrypt)
    filename = getInputFile()
    decrypted_message = decrypt(filename)
    print("The decrypted message is: ")
    print(decrypted_message)

if __name__ == "__main__":
    main()
