import io
import unittest
from unittest import mock
import pytest
from app.LichessGameDownloader import LichessGameDownloader
from app.GameAnalysisEngine import GameAnalysisEngine

def test_suspicious_game(get_sample_pgn):
    testGameDownloader = LichessGameDownloader()
    testGameDownloader.pgn = get_sample_pgn
    test_pgn = get_sample_pgn
    testEngine = GameAnalysisEngine()
    testEngine.load_game(test_pgn)
    print("analyzing game...")
    testEngine.analyze_game()
    print("DONE")