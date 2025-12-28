# 🕹️ Pong with Pygame
A polished, arcade-style 2D Pong experience built with Python and Pygame. This version features progressive difficulty, ball spin mechanics, and a clean modular codebase.

## 📁 Project Structure
The project is split into modules for better maintainability and organized assets:

- ``main.py:`` The core game loop and logic.

- ``constants.py:`` Game settings, colors, and initial object dimensions.

- ``sounds/:`` Dedicated folder for audio assets (.wav format for macOS compatibility).
## Getting Started
Prerequisites
Ensure you have Python 3 and the Pygame library installed:

```bash
    pip install pygame
```
## How to Run
Ensure your sound files are located inside the sounds/ directory.
Run the game from the root folder:
```bash
    python main.py
```
## 🎮 Controls
| Action | Player 1 (Left) | Player 2 (Right) |
| :--- | :--- | :--- |
| **Move Up** | `W` | `Up Arrow` |
| **Move Down** | `S` | `Down Arrow` |
| **Start Game** | `Space` | `Space` |
| **Pause Game** | `P` | `P` |
| **Restart (Win Screen)** | `R` | `R` |
## 🛠️ Advanced Features
- Dynamic Ball Spin: The ball's return angle changes based on where it strikes the paddle (top, center, or bottom), allowing for strategic aiming.
- Progressive Difficulty: The ball accelerates by 10% with every paddle hit.
- Handicap Shrinking System: When a player scores, their own paddle shrinks by 10 pixels (down to a minimum of 40), making it harder to defend a lead.
- State Management: Includes a Start Screen, Pause functionality (P), and a Win Screen with a restart option.
- Arcade Visuals: Features a translucent dashed center line and a specialized UI for score and win messages.
- Audio Feedback: Dedicated sounds for paddle bounces, scoring, and victory.
## 🔧 Technical Details
- Framerate: Locked at 60 FPS for smooth movement.
- Physics: Uses Pygame’s Rect collision system combined with manual velocity adjustments for spin and acceleration.
- Encapsulation: Game constants are decoupled from logic to allow for easy balancing of speed and scoring.