# Maze Path Visualizer 🏁🔍

This Python project implements the **A* algorithm** to find the shortest path in a randomly generated maze. It visualizes the pathfinding process by creating a **GIF animation** of the algorithm's progress, from start to goal.

## Features ✨
- **Maze Generation**: Random maze with obstacles and weighted paths.
- **A* Pathfinding**: Finds the optimal path from start to goal.
- **GIF Visualization**: Visualizes each step of the algorithm in a GIF.
- **Customizable Parameters**: Adjust maze size, obstacle density, and weighted paths.

## How It Works 🛠️
1. A random maze is generated with obstacles (`#`) and weighted paths (`1-5`).
2. The **A* algorithm** computes the shortest path from the start to the goal.
3. A **GIF** is generated, showing each step of the pathfinding process.
   - 🟩 Start Position
   - 🟥 Goal Position
   - 🔵 Explored Path

## Installation & Usage 🚀
1. Install dependencies:
   ```bash
   pip install pillow pygame
