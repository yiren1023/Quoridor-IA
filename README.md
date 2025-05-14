# Quoridor-IA

Quoridor AI – Main Interface (Main.py)

This project provides an interface to train, save, load, and use an artificial intelligence model for the game of Quoridor.

Main Features

The Main class allows you to:

- ✅ Create a neural network-based AI
- 💾 Load/Save the AI from/to a `.npz` file
- 🧠 Train the AI using different reinforcement learning strategies:
  - Q-learning
  - TD-lambda
- 🧪 Compare two AI models
- 🎮 Play a game:
  - Human vs AI
  - Human vs Human

Technologies and Concepts Used

- Python with NumPy
- Simple neural network with two weight matrices (`W1`, `W2`)
- Reinforcement learning (Q-learning, TD-lambda)
- Board and wall management using graph structure
- Save/load models using `np.savez` / `np.load`

Quick Usage Example

Here is a typical usage in an external script or interface:

```python
game = Main()
game.create(neurons_hidden=64, board_size=9, wall_count=10)
agents = game.train_IA(eps=0.1, alpha=0.01, lamb=0.9, ls='Q-learning')
```

To save or load the AI:
```python
game.save_file("my_ai.npz")
game.load_file("old_model.npz")
```

To start a game:
```python
game.play_human_vs_IA()
game.play_human_vs_human(board_size=9, wall_count=10)
```

Dependencies

- numpy

```bash
pip install numpy
```

AI Structure

The AI is represented by a pair `(W1, W2)` corresponding to the weight matrices of a two-layer neural network.

Notes

- The global state of the game is handled using global variables (`N`, `WALLS`, `EPS`, `ALPHA`, `LAMB`, etc.), which may make integration with other modules less straightforward.
- This module does NOT include implementations for `Player_AI`, `Player_Human`, `computeGraph`, or `play`: these components must exist in your project for full functionality.
