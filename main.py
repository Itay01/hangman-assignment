from pictures import HANGMAN_ASCII_ART, HANGMAN_PHOTOS

MAX_TRIES = 6


def main():
    """Main function. Run the hangman game, by using the other functions."""
    print(f"{HANGMAN_ASCII_ART}\nMax tries: {MAX_TRIES}\n")

    secret_word = opening_screen()

    failed_attempts = 0
    old_letters_guessed = []

    game_on = True
    while game_on:
        letter = input("Guess a letter: ").lower()
        letter_valid = try_update_letter_guessed(letter, old_letters_guessed)
        if letter_valid is not False:
            old_letters_guessed = letter_valid

            if letter not in secret_word:
                failed_attempts += 1
                print(f":(\n{print_hangman(failed_attempts + 1)}")

            print(show_hidden_word(secret_word, old_letters_guessed))

        if failed_attempts == MAX_TRIES:
            print(f"\nThe word was {secret_word}")
            game_on = False

        if check_win(secret_word, old_letters_guessed):
            print("WIN")
            game_on = False


def opening_screen():
    """The function prints the opening screen. Return the word for the game."""
    word_valid = choose_word()[1]
    while word_valid is False:
        word_valid = choose_word()[1]

    chosen_word = word_valid

    print("\nLet’s start!")

    print(print_hangman(1))
    print(len(chosen_word) * "_ " + "\n")

    return chosen_word


def choose_word():
    """The function asks the user for the text file path, and the index of the word.
    Return a tuple of with the number of words in the text file, and the word the user choose.
    In case the text file path, or the index of the word is invalid,
    the function will print an error message, and return a tuple with the error (str), and False (bool)."""
    file_path = input("Enter file path: ")
    index = input("Enter index: ")

    try:
        with open(file_path, 'r') as file:
            file_list = file.read().split(" ")
            words_list = list(dict.fromkeys(file_list))

            list_len = len(words_list)
            chosen_word = words_list[int(index) % list_len]

            return_tuple = (list_len, chosen_word)
            return return_tuple
    except FileNotFoundError:
        print("The file path you entered does not exist. Please try again!\n")
        return "invalid file path", False
    except ValueError:
        print("The word index you entered is invalid. Please try again!\n")
        return "invalid word index", False


def check_valid_input(letter_guessed, old_letters_guessed):
    """The function checks if the letter the user entered is valid. If so, the function will return True (bool). Else,
    the function will return False (bool)."""
    if len(letter_guessed) > 1 or not letter_guessed.isalpha():
        return False
    elif letter_guessed in old_letters_guessed:
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """The function uses the function 'check_valid_input' to check if the letter the user entered is valid.
    If the letter is valid, the function will add the letter to the list and return it.
    If the letter is invalid, the function will return False (bool). In that case it will print 'X',
    and an alphabetical list of the letters that were guessed, separated by ' -> '."""
    if check_valid_input(letter_guessed, old_letters_guessed):
        old_letters_guessed.append(letter_guessed)
        return old_letters_guessed

    sorted_list = sorted(old_letters_guessed)
    separated_list = " -> ".join(sorted_list)
    print(f"X\n{separated_list}")
    return False


def print_hangman(num_of_tries):
    """The function returns a picture of the hangman, based on the failed attempts of the user."""
    return HANGMAN_PHOTOS[f"picture {num_of_tries}"]


def show_hidden_word(secret_word, old_letters_guessed):
    """The function compares the letters the user guessed to the chosen word. It loops through the word,
    and check each letter if the user guessed it. If the user did guess it, it will add the letter to the string.
    If not, it will replace the letter with '_'. Return a string with the letters the user guessed,
    and '_' instead of the letter in the chosen word, that the user did not guess."""
    solution_word = []
    for letter in secret_word:
        if letter in old_letters_guessed:
            solution_word.append(letter)
        else:
            solution_word.append("_")
    return " ".join(solution_word)


def check_win(secret_word, old_letters_guessed):
    """The function checks if the user guessed all the letters in the word.
    Return True (bool) if the user did guess all the letters, and False (bool) if the user did not."""
    for letter in secret_word:
        if letter not in old_letters_guessed:
            return False
    return True


if __name__ == '__main__':
    main()
