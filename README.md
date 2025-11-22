# **🐦 Flappy Bird**

A classic arcade-style game built using Python and the Pygame library, featuring a unique "Pillar" aesthetic and the scoring mechanic of 1 point per pillar passed.

## **🚀 Getting Started**

Follow these steps to set up and run the game on your local machine.

### **Prerequisites**

You need to have Python installed on your system. This game requires the pygame library.

\# Install Pygame via pip  
pip install pygame

### **Installation and Setup**

1. **Download the Code:** Save the provided Python code as flappy\_bird.py.  
2. **Add Assets:** Ensure the following image files are placed in the **same directory** as your flappy\_bird.py script:  
   * bird.png (The player character)  
   * pilar.png (The obstacles)  
   * background.png (The game background)  
3. **Run the Game:** Execute the script from your terminal:

python flappy\_bird.py

## **🕹️ How to Play**

The goal is to navigate the bird through the gaps between the pillars without hitting any of them or the ground/ceiling.

### **Controls**

| Action | Key/Input |
| :---- | :---- |
| **Flap Up** | **SPACEBAR** or **Mouse Click** |
| **Start Game** | **SPACEBAR** or **Mouse Click** (from the start screen) |
| **Restart Game** | **SPACEBAR** or **Mouse Click** (from the game over screen) |

### **Scoring**

You gain **1 point** for every pillar that successfully passes the bird's horizontal position. Your score is displayed in the top-left corner of the screen.

## **🛠️ Code Structure Overview**

The game logic is entirely contained within flappy\_bird.py and structured using Object-Oriented Programming (OOP) principles:

* **Bird Class:** Handles gravity, vertical movement, rotation, and flapping.  
* **Pillar Class:** Manages the creation, movement, and drawing of the top and bottom pillar segments, including the random gap positioning.  
* **Main Loop:** Manages the game states (start, playing, game\_over), handles user input, checks for collisions, and controls pillar spawning.

Enjoy the game\!
