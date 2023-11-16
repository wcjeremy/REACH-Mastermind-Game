#Jeremiah Gadingan
#REACH BACKEND TAKEHOME PROJECT
#Mastermind Game
#MULTI PLAYER VERSION

import requests
import time

class MastermindGame:
    # mapping difficulty levels: number of digits, min value, max value
    difficultyMapping = {"easy": (3, 0, 5), "medium": (4, 0, 7), "hard": (5, 0, 9)}

    def __init__(self, difficulty="medium"):
        # constructor/initializer for the start of the game
        self.difficulty = difficulty.lower()
        self.secretPattern = self.generateSecretPattern()  # generate the SECRET CODE!
        self.maxAttempts = 10 # Max number of attempts allowed as per the prompt
        self.attemptsLeft = self.maxAttempts
        self.guessHistory = []  # stores tuples of (guess, feedback, time taken)
        self.playerTurn = 1  # multiplayer addition tracks the current player's turn in multiplayer mode
        self.playerScores = {1: 0, 2: 0}  # Store the scores of each player
        self.startTime = None  # stores the start time of the game
        self.endTime = None  # will stores the end time of the game

    def generateSecretPattern(self):
        # Generate a secret pattern using an external API, based on current difficulty
        numDigits, minVal, maxVal = self.difficultyMapping[self.difficulty]
        url = "https://www.random.org/integers/"
        params = {
            "num": numDigits, "min": minVal, "max": maxVal,
            "col": 1, "base": 10, "format": "plain", "rnd": "new"
        }
        response = requests.get(url, params=params) #call the url using the parameters
        return [int(num) for num in response.text.strip().split('\n')] #turn the response into an interger

    def calculateScore(self, player):
        # Calculates the score based on remaining attempts/ max attempts and difficulty
        scoreMapping = {"easy": 100, "medium": 200, "hard": 300} #base values for scores
        return scoreMapping[self.difficulty] * (self.attemptsLeft / self.maxAttempts)

    def provideHint(self):
        # provides hints based on the number of remaining attempts
        if self.attemptsLeft == 8:
            print(f"\nHint: One of the numbers in the secret pattern is {self.secretPattern[1]}")
        elif self.attemptsLeft == 5:
            print(f"\nHint: One of the numbers in the secret pattern is {self.secretPattern[0]}")
        elif self.attemptsLeft == 2:
            print(f"\nHint: The last number in the secret pattern is {self.secretPattern[-1]}")

    def displayHistory(self):
        # displays the history of all guesses along with feedback and duration
        print("\nFeedback History:")
        for guess, feedback, duration in self.guessHistory:
            print(f"Player: {guess} Gate Keeper: {feedback} [Duration: {duration}]")

    def displayAttemptsLeft(self):
        # Displays the number of attempts remaining
        print(f"Attempts left: {self.attemptsLeft}")

    def provideFeedback(self, guess):
        # Compares player's guess with secret pattern and provides feedback
        correctPositions = sum(1 for p, g in zip(self.secretPattern, guess) if p == g) # counter of numbers in correct positions
        correctNumbers = sum(1 for num in guess if num in self.secretPattern)  # counter of correct numbers not worring about position
        return correctNumbers, correctPositions

    def initializeGame(self):
        # Initialize game settings based on player's difficulty
        print("\n[Gate Keeper: 'Welcome, Players. Which of you is the Mastermind? Who will unlock the code?']")
        while True: #loop
            self.difficulty = input("Choose difficulty (Easy, Medium, Hard): ").lower()
            if self.difficulty in self.difficultyMapping:
                break # Break the loop if a valid difficulty is selected
            else:
                print("Invalid difficulty level. Please enter 'easy', 'medium', or 'hard'.")
        print(f"Selected difficulty: {self.difficulty.capitalize()}")
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

                # Check if the guess length matches the secret pattern length
                if len(guess) == len(self.secretPattern):
                    return guess
                else:
                    # Inform the player about the expected number of digits
                    print(f"Invalid input. Please enter {len(self.secretPattern)} numbers separated by spaces.")
            except ValueError:
                # This will catch non-integer inputs
                print("Invalid input. Please enter numeric values.")

    def processGuess(self, guess):
        # Process player guess, providefeedback, and updates game history
        correctNumbers, correctPositions = self.provideFeedback(guess)
        feedback = f"{correctNumbers} correct number{'s' if correctNumbers != 1 else ''}, " \
                   f"{correctPositions} in the correct position{'s' if correctPositions != 1 else ''}."
        guessDuration = time.time() - self.startTime
        formattedDuration = time.strftime("%M minutes and %S seconds", time.gmtime(guessDuration))
        self.guessHistory.append((guess, feedback, formattedDuration))
        self.displayHistory()
        return correctNumbers, correctPositions

    def displayInitialInfo(self):
        # Display initial game information based on the selected difficulty level
        minVal, maxVal = self.difficultyMapping[self.difficulty][1:3]
        print("\nGame initializes and selects", " ".join(map(str, self.secretPattern)))
        print("Gate Keeper: Welcome, Players. Are you the Mastermind, can you unlock the code?")
        print(f"Guess the {len(self.secretPattern)}-digit pattern (Digits between {minVal} and {maxVal}).")

    def saveHighScores(self, highScores, filename):
        # Save the high scores to an external file, including the player name
        with open(filename, "w") as file:
            for score, name in highScores:
                file.write(f"{score:.1f},{name}\n")

    def loadHighScores(self, filename):
        try:
            with open(filename, "r") as file:
                return [(float(score), name) for score, name in (line.strip().split(',') for line in file)]
        except FileNotFoundError:
            return []

    def displayHighScores(self, filename):
        # displays the high scores
        highScores = self.loadHighScores(filename)
        print("\nHigh Scores:")
        for score, name in highScores:
            print(f"{name}: {score:.1f}")

    def play(self):
        # main game loop, initializes the game, processes guesses, and ends the game
        self.initializeGame()
        while self.attemptsLeft > 0:
            print(f"Player {self.playerTurn}'s Turn")
            self.provideHint()  # offer hints based on specific attempts
            guess = self.getPlayerGuess()  # prompt the player for a guess
            correctNumbers, correctPositions = self.processGuess(guess)
            # check if the player guess matches the secret pattern!!
            if correctPositions == len(self.secretPattern):
                break  # end the loop if the guess is correct
            self.playerTurn = 2 if self.playerTurn == 1 else 1  # Switch to the next player
            self.attemptsLeft -= 1  # Decrement the number of attempts left
        self.endGame()  # Handle end logic look below

    def endGame(self):
        self.endTime = time.time()
        # Check if any player has guessed the pattern correctly
        if any(score > 0 for score in self.playerScores.values()):
            winningPlayer = max(self.playerScores, key=self.playerScores.get)
            winningScore = self.calculateScore(winningPlayer)  # Calculate the winning score

            highScores = self.loadHighScores("multiplayer_high_scores.txt")
            lowestHighScore = min(highScores, default=(0, ''))[0] if highScores else 0

            if winningScore > lowestHighScore or len(highScores) < 5:
                playerName = input(f"Player {winningPlayer}, you've set a new high score! Enter your name: ")
                highScores.append((winningScore, playerName))
                highScores = sorted(highScores, reverse=True, key=lambda x: x[0])[:5]
                self.saveHighScores(highScores, "multiplayer_high_scores.txt")
        else:
            # No player guessed the pattern correctly
            print("Game over! None of the players guessed the pattern within the allowed attempts.")
            print("The correct pattern was:", " ".join(map(str, self.secretPattern)))

        print(
            f"Game duration: {time.strftime('%M minutes and %S seconds', time.gmtime(self.endTime - self.startTime))}")

# start the mastermind class and play the game
if __name__ == "__main__":
    while True:
        game = MastermindGame()
        game.displayHighScores("multiplayer_high_scores.txt") # display high scores at the start
        game.play() # start a new game
        playAgain = input(f"\n...Play again? (Yes/No): ") #ask if player wants to go again
        if playAgain.lower() != 'yes':
            break # exit the loop and end the program if player does not want to replay