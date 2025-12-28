# 🕹️ Pong with Pygame

A classic 2D Pong game built using Python and the Pygame library. This project features a smooth 60 FPS gameplay experience, dual-player controls, and randomized ball physics.

## Getting Started

## Prerequisites
You will need Python 3 and the Pygame library installed on your machine.
```bash
    pip install pygame
```
### How to Run
1. Clone this repository to your local machine.
2. Navigate to the project folder in your Terminal.
3. Run the game:
```bash
    python main.py
```

## 🎮 Controls
| Player | Move Up | Move Down |
| :--- | :--- | :--- |
| **Player 1 (Left)** | `W` | `S` |
| **Player 2 (Right)** | `Up Arrow` | `Down Arrow` |

## 🛠️ Features
- Dynamic Physics: The ball bounces off walls and paddles with randomized starting trajectories.
- Mac Optimized: Includes a frame rate clock and proper display flipping to ensure stability on macOS.
- Collision Detection: Utilizes Pygame's Rect system for precise paddle and wall bounces.
- Auto-Reset: The ball resets to the center automatically after a point is scored.
- Scoreboard: The Scoreboard updates after a point is scored. After one Player achieves ten points a Win message will be displayed.