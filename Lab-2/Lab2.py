def getInputFile():
    """Ask the user for a file name, check if it ends with '.txt', and return it."""
    filename = input('Enter the name of your file: ')
    if filename.endswith('.txt'):
        return filename
    else:
        print('Invalid file name. Please enter a valid filename.')
        return getInputFile()


def decrypt(filename):
    """Decrypt a message from a file using a Caesar cipher."""
    with open('secretMessage1.txt', 'r') as file:
        shift = int(file.readline().strip())
        secret_Message = file.readline().strip().split()
    decrypted_message = ""
    for word in secret_Message:
        decrypted_word = ""
        for char in word:
            decrypted_char = chr((ord(char.lower()) - ord('a') - shift) % 26 + ord('a'))
            decrypted_word += decrypted_char
        decrypted_message += decrypted_word + " "
    print("The decrypted message is:\n" + decrypted_message)

def main():
    filename = getInputFile()
    decrypt(filename)

if __name__ == "__main__":
    main()

