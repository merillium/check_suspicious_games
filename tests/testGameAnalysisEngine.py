import pytest
from app.LichessGameDownloader import LichessGameDownloader
from app.GameAnalysisEngine import GameAnalysisEngine

def testGameAnalysisEngine(getGameCode):
    try:
        testGameDownloader = LichessGameDownloader()
        testGameDownloader.get_game(getGameCode)
        testPGN = testGameDownloader.pgn
        testEngine = GameAnalysisEngine()
        testEngine.load_game(testPGN)
        testEngine.analyze_game()
    except ValueError as e:
        print(f"Caught exception {e}")


    