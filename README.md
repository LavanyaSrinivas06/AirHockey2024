# AirHockey

# Air Hockey Game
Overview
Welcome to the Air Hockey Game! This project is a classic air hockey simulation built using Python and Pygame. The game features two paddles, a puck, and a scoreboard, providing a fun and interactive experience for two players.

# Key Features
Player Controls: Control the paddles with the keyboard:
Player 1: W, A, S, D for up, left, down, and right movements respectively.
Player 2: Arrow keys (UP, LEFT, DOWN, RIGHT) for directional control.
Sound Effects: Enjoy realistic sound effects with:
paddle_hit.wav for when the puck hits a paddle.
goal.wav for when a goal is scored.
## Game Mechanics:
The game starts with the puck in the center.
Players score by getting the puck into the opponent's goal.
The game is limited to 5 rounds, with the first player to reach a specific score winning.
Scoring: Scores are displayed on the screen. The game announces the winner at the end and displays the final scores.
# Goal
The objective of the game is to score more goals than your opponent within 5 rounds. Each round ends when the puck crosses into one of the goals, and the game resets with the puck at the center and paddles in their starting positions. The player with the highest score at the end of 5 rounds wins.

## Installation

To install AirHockey, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/LavanyaSrinivas06/AirHockey2024.git
   cd AirHockey2024
2. **Create a virtual environment**
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
3. **Install the dependencies**:
    pip install -r requirements.txt
4. **to run this program**:
    python main.py
5. **running test**:
    pytest
    pytest test.py
    pytest test_background.py
    pytest test_paddle.py
    pytest test_puck.py

# Controls
    Player 1:

    Move Up: W
    Move Down: S
    Move Left: A
    Move Right: D

    Player 2:

    Move Up: UP Arrow Key
    Move Down: DOWN Arrow Key
    Move Left: LEFT Arrow Key
    Move Right: RIGHT Arrow Key
Quit Game: Press Q at any time.

**License**
This project is licensed under the MIT License - see the LICENSE file for details.

**Acknowledgments**
Pygame library for game development.
Open-source resources for sound effects.