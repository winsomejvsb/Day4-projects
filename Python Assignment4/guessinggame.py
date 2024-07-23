import random

def guessing_game():
    # Generate a random number between 1 and 100
    number = random.randint(1, 100)
    attempts = 3

    print("Welcome to the Guessing Game!")
    print("Guess the number between 1 and 100. You have 3 attempts.")

    for attempt in range(1, attempts + 1):
        guess = int(input(f"Attempt {attempt}: Enter your guess: "))

        if guess == number:
            print("You won!")
            return
        elif guess > number:
            print(f"The number you guessed is greater than the number. The number is: {number}")
        elif guess < number:
            print(f"The number you guessed is less than the number. The number is: {number}")

    print("You have used all attempts. Game over!")

if __name__ == "__main__":
    guessing_game()
