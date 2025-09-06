# check_suspicious_games

This is a work-in-progress app that locates and downloads a lichess pgn through the lichess API, then analyzes move times and evaluation changes to flag suspicious moves or behavior.

## Background

Although average centipawn loss can be a good way to flag cheaters, it will only work for the most obvious cases.

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
