# check_suspicious_games

This is a work-in-progress app that locates and downloads a lichess pgn through the lichess API, then analyzes move times and evaluation changes to flag suspicious moves or behavior.

## Background

Although average centipawn loss can be a good way to flag cheaters, it will only work for the most obvious cases.

## Installing Dependencies
To install dependencies, run the following command:
```bash
pip install -r requirements.txt
```

## Tests
To execute unit tests, run the following command:
```bash
pytest -s tests/*.py
```

## To-do
- fix tests so that we can mock returning a pgn from lichess API, but don't make a GET request every time we run a test
- finish basic version of app that supports pgn file upload, and error handling
- thorough tests from preloaded pgns to serve as training for basic suspicious move detection
- error handling for clicking Analyze game without loading a game first

## App Layout Design
- the pgn will be displayed but cannot be edited
- how do we show the moves? maybe show the move with comments as the slider is moved
- how do we display suspicious moves? do we use a figure, table, or just display as text?
