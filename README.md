# ttt

This project implements a generalized NxNxD tic-tac-toe game. The game is played on an `N`x`N` grid where players take turns placing either an ❌ or an ⭕. The first player to get `D` of their pieces in a row wins.

This is an instructive project meant to explore the concepts of game AI and search algorithms. It also has the (un)intended consequence of serving as a algo/math heavy code sample for people that want to pay me $$$.

## AI

We use a combination of heuristic and objective approaches to creating an AI that can play this game. In general, if playing against this computer, you will **always** lose or tie.

Since speed is not of major concern to us, this project is in Python (or is it the other way around?). We also avoid certain concepts such as [bitboards](https://en.wikipedia.org/wiki/Bitboard) since the game space is small enough that hacky optimizations are not needed.

Instead we focus on optimizing the actual search algorithms. Heuristics and algorithms used include:

- Minimax search with alpha-beta pruning
	- Search algorithm that attempts to maximize the AIs chance of winning by assuming a perfect adversary
	- Alpha-beta pruning helps slice the search space even further by discarding branches that will not influence the final score
- Maximum search depth + evaluation function
	- We implement a maximum search depth since the number of evaluations grows expoentially with depth
	- Since victory is an objective game state, we first check for that. Otherwise the current board position is evaluated based on some heuristic to suggest the next move.
- Killer heuristic
	- We consider the 'best' move first by keeping state on previous game positions the AI has evaluated. This is more likely to trigger an alpha-beta cutoff and further reduces the search space.
- Transposition tables
	- We cache old game states the the AI has already evaluated in order to reduce recomputing the same values.
- Iterative Deepening
	- Combines depth-first search's space-efficiency and breadth-first search's completeness
	- In conjunction with the killer heuristic + transposition tables, further reduces time complexity of an optimal algorithm.

There are some 'optimizations' made on the atual Python code, mostly in the form of custom serializers/deserializers to quickly duplicate game state.

The AI can be cached between games or even Python sessions. You are basically training it as you play.

## Gameplay

```python
from nxnxd import *

Game(3, 3, mode='1v1').play()

```

![image](https://user-images.githubusercontent.com/2442871/32583985-fd41365a-c4aa-11e7-9705-ab5472041e72.png)

More to come when this is done. GIFs of individual vs computer play.

## Next Steps

- Stochastic search algorithms
	- Can we create parameters that can be tuned and improved via self play?
- Make a chess engine
