![Jeremiah Gadingan](https://github.com/wcjeremy/REACH-Mastermind-Game/assets/116251775/4b029c04-4792-4272-a575-68d559ad0ecd)



## What is Mastermind??
 
Embark on an enthralling journey with the Mastermind Game. Mastermind is a challenging and engaging game where players compete against the computer to crack a numerical code. The objective is simple yet stimulating: guess the correct sequence of numbers within a limited number of attempts. Feedback is provided after each guess, indicating how close the player's guess was to the actual number combination. 
* This is also my project for an amazing program I want to get in! :)

## Why Play Mastermind?

Mastermind is a blend of strategy, logic, and deduction, making it an excellent brain exercise. It's not just about guessing; it's about using logic to interpret feedback and refine subsequent guesses. This game is ideal for those who enjoy puzzles and mental challenges.

## How to Play Mastermind 

Game rules
*	At the start of the game the computer will randomly select a pattern of four different numbers from a total of 8 different numbers.
*	A player will have 10 attempts to guess the number combinations
*	At the end of each guess, computer will provide one of the following response as feedback:
     *	The player had guess a correct number
     *	The player had guessed a correct number and its correct location
     *	The player’s guess was incorrect

* Starting the Game: The computer randomly selects a sequence of numbers based on the chosen difficulty level.
* Making a Guess: Players input their guess for the number sequence. (Note: input your numbers with spaces in between)
* Receiving Feedback: The game provides feedback on the accuracy of the guess - correct numbers and/or correct positions.
* Winning the Game: The goal is to correctly guess the entire sequence within the given attempts.

**Example Run:
Game initializes and selects “0 1 3 5”
    * Player guesses “2 2 4 6”, game responds “all incorrect”
    * Player guesses “0 2 4 6”, game responds “1 correct number and 1 correct location”
    * Player guesses “2 2 1 1”, game responds “1 correct number and 0 correct location”
    * Player guesses “0 1 5 6”, game responds “3 correct numbers and 2 correct location”


## Features

* Random Number Generation: The game uses the Random Number Generator API to create the secret number combinations.
* Language and Libraries: Developed in Python, utilizing requests for API communication and time for gameplay dynamics.
* Singleplarer or Multiplayer versions: Play solo or challenge a friend.
* User Interface: Simple command-line interface for easy interaction and accessibility.
    * Ability to guess the combinations of 4 numbers
    * Ability to view the history of guesses and their feedback
    * The number of guesses remaining is displayed
    * Variable Difficulty Levels: Choose from easy, medium, or hard levels to suit your skill.
    * Feedback System: Intelligent feedback helps players gauge their progress.
    * Timer: There is a clock that displays the minutes and seconds it takes for the entire game AND each guess attempt.



* High Score Tracking: Scores are recorded, allowing players to track their improvement or compete with others.

## Getting Started

1. Clone the Repository: git clone https://github.com/wcjeremy/REACH-Mastermind-Game.git 
2. Install Requirements: Ensure Python and the requests library are installed.
3. Navigate to the Directory: cd REACH-Mastermind-Game
4. Run the Game: Execute python MastermindGame.py in your terminal.
5. HAVE FUN :)


## Some Bugs To Note 

* If name already exists, it will print out the same name multiple times
* More error handling on incorrect inputs:
* Does not give an error when entering in more than 3, 4 , 5  inputs respective to difficulty, instead, code asks for another guess

