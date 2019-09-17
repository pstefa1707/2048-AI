# 2048-AI
Monte Carlo Search Tree implementation for 2048 written in python &amp;&amp; 2048 clone using pygame

# Dependancies
`Python3.4 +`

`pip install pygame`

# Usage
`console.py` is a console visualisation of the AI running, works well with multi-core processing on all operating systems.

`gui.py` is gui visualisation of AI running and also allows user to play, multi-core processing doesn't like windows with pygame :(

Change `AI_ENABLED` variable in `gui.py` to enable or disable the AI, if disabled you can play a normal game of 2048

Change `N_GAMES` variable in either `gui.py` or `console.py` to change the number of games the AI will simulate before making a move, the more games simulated, the better the AI will perform but the slower it will run!

Use `WASD/ARROW` keys if playing without AI running.

# Features

When grid object is made in both `gui.py` and `console.py`, use `width=` and `height=` arguments to change size of 2048 grid, game will automatically adapt :)

# Performance (approx)

`50` look ahead games ~ 1024, 65% of the time and 2048, 10% of the time
`100` look ahead games ~ 1024, 80% of the time and 2048, 25% of the time
`500` look ahead games ~ 1024, 95% of the time and 2048, 40% of the time

# Screenshot

![2048 AI](https://i.ibb.co/Q9RGWy6/download.png)
