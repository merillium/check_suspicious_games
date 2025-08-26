# check_suspicious_games

This is a work-in-progress app that locates and downloads a lichess pgn through the lichess API, then analyzes move times and evaluation changes to flag suspicious moves or behavior.

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