# Maze Solver

This project allows users to draw a maze on a grid and solve it using the A* or BFS (Breadth-First Search) algorithms. The program visually demonstrates how each algorithm works by individually coloring the nodes that the algorithm visits. 

## Features
- **Draw Your Own Maze**: Use the mouse to draw obstacles (walls) on a grid.
- **Choose an Algorithm**: Select between A* and BFS to solve the maze.
- **Algorithm Visualization**: Watch the algorithms in action as they explore the maze, coloring nodes as they go.
- **Grid-based Interface**: The grid provides a simple interface for designing and solving the maze.

## Requirements
To run this project, you need Python installed on your system. This project also uses the `pygame` library for rendering the grid and animations.

## Setup Instructions

1. **Create a Python Virtual Environment**:
   - Navigate to your project directory in the terminal.
   - Run the following command to create a virtual environment:
     ```bash
     python -m venv venv
     ```
   
2. **Activate the Virtual Environment**:
   - On Windows, use:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS or Linux, use:
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   - Install the required dependencies using pip:
     ```bash
     pip install pygame
     ```

4. **Run the Program**:
   - To run the program, simply execute the `main.py` file:
     ```bash
     python main.py
     ```
