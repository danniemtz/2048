# 2048
The 2048 game as played on the web
Language/Tool ver. : Python 3.13
No dependencies needed to install


**How to play**
- You are prompted with a couple of options (WASD)
- the board will move according to your choice, try to group like numbers together
- the goal is to get 2048 on the board with your combinations
- Key	Action
W	Move Up
A	Move Left
S	Move Down
D	Move Right
Q	Quit the Game


**What I implemented**
- The move_left,right,up,down functions
- The main game loop that asks for user input and renders the board according to the user input
- Board initialization with random tiles
- Win detection (2048 tile reached)
- Loss detection (no valid moves left)
- Clear terminal board display for better readability
- Full deterministic testing (test_seed.py)


**How to Run**
- Type in terminal:  python3 game.py
- To run test seed file (no need for seeding the file, it does it inside), just type in terminal: python3 test_seed.py


**Challenges**
- Designing deterministic tests to verify game consistency
- Handling user input and console-based UI updates in a loop
- Creating a stagnant board to show up on the terminal (os), wont have to display a new board with every move


