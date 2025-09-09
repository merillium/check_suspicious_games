# check_suspicious_games

This is a work-in-progress app that locates and downloads a lichess pgn through the lichess API, then analyzes move times and evaluation changes to flag suspicious moves or behavior.

## Background

Although average centipawn loss is a meaningful metric to help flag potential cheaters, it will only work for the most obvious cases where a person cheats on every move. Players who want to evade cheat detection will typically either (1) mix their own moves with computer moves, or (2) examine computer moves and select suboptimal choices. I will mention in passing that a genuinely strong player who uses computer assistance to cheat infrequently enough (e.g. using a computer every few games, at only a small number of critical points) is essentially undetectable. However, putting this edge case aside, most players using computer assistance are not simply not strong enough to judge the degree to which moves are obvious to strong players, and this is often how strong players facing cheaters will sense something is off.

## Methods

There are few hallmarks of cheating that this app attempts to help users flag suspicious behavior from a game: (1) unusually long think times for obvious moves, (2) unusually short think times for critical moves. Neither of these things are conclusive, but this app is meant to be a tool to help users report games they believe are suspicious, and provide more in depth move classification than lichess computer analysis.

## Installing Dependencies
To install dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Running the App
To run the app locally, cd into the app directory and then run the command:
```python app.py```

## Tests
To execute unit tests, run the following command:
```bash
pytest -s tests/*.py
```

## To-do + Error Handling
- fix tests so that we can mock returning a pgn from lichess API, but don't make a GET request every time we run a test
- finish basic version of app that supports pgn file upload, and error handling
- thorough tests from preloaded pgns to serve as training for basic suspicious move detection
- error handling for clicking Analyze game without loading a game first
- check whether a game is blitz or rapid. bullet game analysis is probably not reliable
- check that timestamps are included, throw an error if not (or provide analysis without timestamps, but this is less reliable)
- still issues analyzing a pgn when a player resigns on the opponent's move

## App Layout Design
- moves on the board are controlled by forward and backward arrows
- display moves and labels using a table, possibly add comments
