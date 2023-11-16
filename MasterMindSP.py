#Jeremiah Gadingan
#REACH BACKEND TAKEHOME PROJECT
#Mastermind Game
#SINGLE PLAYER VERSION

import requests #we use this library to communicate with urls
import time #used to get the time

class MastermindGame:
    # mapping difficulty levels: number of digits, min value, max value
    difficultyMapping = {"easy": (3, 0, 5), "medium": (4, 0, 7), "hard": (5, 0, 9)}

    def __init__(self, difficulty="medium"):
        # constructor/initializer for the start of the game
        self.difficulty = difficulty.lower()
        self.secretPattern = self.generateSecretPattern()  # generate the SECRET CODE!
        self.maxAttempts = 10  # Max number of attempts allowed as per the prompt
        self.attemptsLeft = self.maxAttempts
        self.guessHistory = []  # stores tuples of (guess, feedback, time taken)
        self.score = 0
        self.startTime = None  # stores the start time of the game
        self.endTime = None  # will stores the end time of the game

    def generateSecretPattern(self):
        # Generate a secret pattern using an external API AND based on current difficulty
        numDigits, minVal, maxVal = self.difficultyMapping[self.difficulty]
        url = "https://www.random.org/integers/"
        params = {
            "num": numDigits,  # Number of digits in the pattern
            "min": minVal,     # Minimum value of each digit
            "max": maxVal,     # Maximum value of each digit
            "col": 1,          # Number of columns (1 - single column of numbers)
            "base": 10,        # Base 10 (decimal)
            "format": "plain", # Plain text format
            "rnd": "new"       # Request for new random numbers
        }
        response = requests.get(url, params=params) #call the url using the parameters
        return [int(num) for num in response.text.strip().split('\n')] #turn the response into an interger

    def calculateScore(self):
        # Calculates the score based on remaining attempts/ max attempts and difficulty
        scoreMapping = {"easy": 100, "medium": 200, "hard": 300} #base values for scores
        self.score = scoreMapping[self.difficulty] * (self.attemptsLeft / self.maxAttempts)

    def provideHint(self):
        # provides hints based on the number of remaining attempts
        if self.attemptsLeft == 8:
            print(f"\nHint: One of the numbers in the secret pattern is {self.secretPattern[1]}")
        elif self.attemptsLeft == 5:
            print(f"\nHint: One of the numbers in the secret pattern is {self.secretPattern[0]}")
        elif self.attemptsLeft == 2:
            print(f"\nHint: The last number in the secret pattern is {self.secretPattern[-1]}")

    def displayHistory(self):
        # display history of all guesses along with feedback and duration
        print("\nFeedback History:")
        for guess, feedback, duration in self.guessHistory:
            print(f"Player: {guess} Gate Keeper: {feedback} [Duration: {duration}]")

    def displayAttemptsLeft(self):
        # Display number of attempts remaining
        print(f"Attempts left: {self.attemptsLeft}")

    def provideFeedback(self, guess):
        # Compare player's guess with secret pattern and provides feedback
        correctPositions = sum(1 for p, g in zip(self.secretPattern, guess) if p == g)  # counter of numbers in correct positions
        correctNumbers = sum(1 for num in guess if num in self.secretPattern)  # counter of correct numbers not worring about position
        return correctNumbers, correctPositions

    def initializeGame(self):
        # Initialize game settings based on player's difficulty
        print("Welcome to Mastermind!")
        while True: #loop
            self.difficulty = input("Choose your difficulty level: Easy, Medium, Hard\nEnter difficulty level: ").lower()
            if self.difficulty in self.difficultyMapping:
                break  # Break the loop if a valid difficulty is selected
            else:
                print("Invalid difficulty level. Please enter 'easy', 'medium', or 'hard'.")
        print(f"\nSelected difficulty: {self.difficulty.capitalize()}")
        self.secretPattern = self.generateSecretPattern()  # Generate a new secret pattern
        self.attemptsLeft = self.maxAttempts
        self.startTime = time.time()  # Record the start time of the game
        self.displayInitialInfo()

    def getPlayerGuess(self):
        # Prompt player for a guess and validates the input
        while True:
            guessInput = input("Enter your guess (separated by spaces): ")
            try:
                guess = [int(num) for num in guessInput.split()]
                if len(guess) == len(self.secretPattern):
                    return guess
            except ValueError:
                print("Invalid input. Please enter numeric values.")

    def processGuess(self, guess):
        # Process player guess, providefeedback, and updates game history
        correctNumbers, correctPositions = self.provideFeedback(guess)
        feedback = f"{correctNumbers} correct number{'s' if correctNumbers != 1 else ''}, " \
                   f"{correctPositions} in the correct position{'s' if correctPositions != 1 else ''}."
        guessDuration = time.time() - self.startTime
        formattedDuration = time.strftime("%M minutes and %S seconds", time.gmtime(guessDuration)) #format for time!
        self.guessHistory.append((guess, feedback, formattedDuration))
        self.displayHistory()
        return correctNumbers, correctPositions

    def displayInitialInfo(self):
        # Display initial game information based on the selected difficulty level
        minVal, maxVal = self.difficultyMapping[self.difficulty][1:3]
        print("Game initializes and selects", " ".join(map(str, self.secretPattern)))
        print("Gate Keeper: Welcome, Player. Are you the Mastermind, can you unlock the code?")
        print(f"To unlock the gate, you must guess the {len(self.secretPattern)}-number combination! (Numbers between {minVal} and {maxVal} separated by spaces)")

    def saveHighScores(self, highScores):
        # Save the high scores to an external file, including the player name
        with open("high_scores.txt", "w") as file:
            for score, name in highScores:
                file.write(f"{score:.1f},{name}\n")

    def loadHighScores(self):
        # Load the high scores from the external file
        try:
            with open("high_scores.txt", "r") as file:
                highScores = []
                for line in file:
                    parts = line.strip().split(',')
                    if len(parts) == 2:
                        score, name = parts
                        highScores.append((float(score), name))
                return highScores
        except FileNotFoundError:
            return [] #if nothing is found just say nothing

    def displayHighScores(self):
        # displays the high scores
        highScores = self.loadHighScores()
        print("High Scores:")
        for score, name in highScores:
            print(f"{name}: {score:.1f}")

    def play(self):
        # main game loop, initializes the game, processes guesses, and ends the game
        self.initializeGame()
        while self.attemptsLeft > 0:
            self.provideHint()  # offer hints based on specific attempts
            guess = self.getPlayerGuess()  # prompt the player for a guess
            correctNumbers, correctPositions = self.processGuess(guess)
            # check if the player guess matches the secret pattern!!
            if correctPositions == len(self.secretPattern):
                break  # end the loop if the guess is correct
            self.attemptsLeft -= 1  # reduce the number of attempts left
        self.endGame()  # Handle end logic look below

    def endGame(self):
        #  end of the game, calculates the score, and checks for high scores
        self.endTime = time.time()
        if self.attemptsLeft > 0:
            self.calculateScore()
            print("*The Gate Unlocks*")
            print("Gate Keeper: You've guessed the correct pattern? You did it, you are the MASTERMIND!")
            print(f"Your score: {self.score}")
            print(f"Total game duration: {time.strftime('%M minutes and %S seconds', time.gmtime(self.endTime - self.startTime))}")
            #logic for highscores
            highScores = self.loadHighScores()
            lowestHighScore = min(highScores, default=(0, ''))[0] if highScores else 0
            if len(highScores) < 5 or self.score > lowestHighScore:
                playerName = input("Congratulations! You've set a new high score! Enter your name: ")
                highScores.append((self.score, playerName))
                highScores = sorted(highScores, reverse=True, key=lambda x: x[0])[:5]
                self.saveHighScores(highScores)
        else:
            print("Game over! You've run out of attempts. The correct pattern was:",
                  " ".join(map(str, self.secretPattern))) #if player runs out of attempts
            print(f"Total game duration: {time.strftime('%M minutes and %S seconds', time.gmtime(self.endTime - self.startTime))}")

# start the mastermind class and play the game
if __name__ == "__main__":
    while True:
        game = MastermindGame()
        game.displayHighScores()  # display high scores at the start
        game.play()  # start a new game
        playAgain = input("\n...Play again? (Yes/No): ") #ask if player wants to go again
        if playAgain.lower() != 'yes':
            break  # exit the loop and end the program if player does not want to replay
