# ChessBot

A simple command-line ChessBot using `python-chess` and a basic minimax with alpha-beta pruning.

## Project structure
```
analyzer.py    # engine: evaluation + minimax search
app.py         # CLI to play vs the AI
README.md
requirements.txt
```

## Requirements
- Python 3.8+
- `python-chess`

Install:
```
pip install -r requirements.txt
```

## Usage
Play vs the AI:
```
python app.py --depth 3 --human-color white
```
- `--depth` controls search depth. Higher values increase strength but are slower.
- Enter moves in **UCI** format (e.g. `e2e4`, `g1f3`, or `e7e8q` for promotion).

## Notes & improvements
- The evaluation function is simple (material + mobility). You can improve strength by adding piece-square tables, quiescence search, iterative deepening, move ordering, transposition tables, etc.
- Depth 3 is a good balance for quick play. Increase to 4 or 5 if you want a stronger engine (but it will take longer).
