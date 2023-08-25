import pickle
import random
import threading


CHOICES = {"Countries", "Chemical Elements", "Fruits and Vegetables"}
DIFF_CHOICES = {"easy", "hard"}
RE_PROMPT = "Wrong choice, please choose from {} or type Quit to exit."

def get_word():
    category = input('Please select a category, Countries / Chemical Elements  / Fruits and Vegetables:\n')
    if category.lower() == "quit":
        exit()
    elif category.lower() == 'chemical elements':
        myfile = open("CHEMICAL_ELEMENTS.dat", "rb")
        master_list = pickle.load(myfile)
        myfile.close()
    elif category.lower() == 'countries':
        myfile = open("COUNTRIES.dat", "rb")
        master_list = pickle.load(myfile)
        myfile.close()
    elif category.lower() == 'fruits and vegetables':
        myfile = open("FRUITS_AND_VEGETABLES.dat", "rb")
        master_list = pickle.load(myfile)
        myfile.close()
    else:
        print(RE_PROMPT.format(list(CHOICES)))
        return get_word()
    difficulty = input("Please choose a difficulty level from Easy or Hard:\n")
    if {difficulty.lower()} <= DIFF_CHOICES:
        difficult = False if difficulty.lower() == "easy" else True
    else:
        print(RE_PROMPT.format(list(DIFF_CHOICES)))
        return get_word()
    return dict(word=random.choice(master_list).upper(), difficult=difficult)

def out_of_time(hint):
    hint["timer"] = True

def display_data(tries, word_completion):
    print(display_hangman(tries))
    print(word_completion)

def fill_word_completion(word_completion, word, guess):
    word_as_list = list(word_completion)
    guessed = False
    indices = [i for i, letter in enumerate(word) if letter == guess]
    for index in indices:
        word_as_list[index] = guess
    word_completion = "".join(word_as_list)
    if "_" not in word_completion:
        guessed = True
    return guessed, word_completion

def play(word, difficult):
    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    hints_taken = 0
    hint_timer = {}
    print("Let's play Hangman!")
    print(display_hangman(tries))
    print(word_completion)
    print("\n")
    while not guessed and tries > 0:
        timer_thread = threading.Timer(
            interval=5, function=out_of_time, args=(hint_timer,)
        )
        timer_thread.start()
        guess = input(
            "Please guess a letter or word, you've got 30 seconds!:"
        ).upper()
        if hint_timer.get("timer"):
            print("You ran out of time in this guess.")
            if hints_taken == 3:
                print("You're out of hints.")
                tries -= 1
                display_data(tries, word_completion)
                continue
            hint_timer["timer"] = False # reset timer flag for next iteration
            if not difficult:
                hint_response = input("Would you like a hint? (Y/N):")
                if "y" in hint_response.lower():
                    remaining_words = list(set(word) - set(guessed_letters))
                    automated_guess = random.choice(remaining_words)
                    guessed_letters.append(automated_guess)
                    guessed, word_completion = fill_word_completion(
                        word_completion, word, automated_guess
                    )
                    display_data(tries, word_completion)
                    hints_taken += 1
                    continue
            tries -= 1
            display_data(tries, word_completion)
            continue
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("You already guessed the letter", guess)
            elif guess not in word:
                print(guess, "is not in the word.")
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                guessed, word_completion = fill_word_completion(
                    word_completion, word, guess
                )
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
        else:
            print("Not a valid guess.")
        display_data(tries, word_completion)
        print("\n")
    if guessed:
        print("Congrats, you guessed the word! You win!")
    else:
        print("Sorry, you ran out of tries. The word was " + word + ". Maybe next time!")


def display_hangman(tries):
    stages = [  # final state: head, torso, both arms, and both legs
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # head, torso, both arms, and one leg
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                # head, torso, and both arms
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                # head, torso, and one arm
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                # head and torso
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                # head
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                # initial empty state
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]


def main():
    word_dict = get_word()
    play(
        word=word_dict.get("word", ""),
        difficult=word_dict.get("difficult", False)
    )
    while input("Play Again? (Y/N): ").lower() == "y":
        word_dict = get_word()
        play(
            word=word_dict.get("word", ""),
            difficult=word_dict.get("difficult", False)
        )


if __name__ == "__main__":
    main()
