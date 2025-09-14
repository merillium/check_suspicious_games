from pandas.testing import assert_frame_equal
import io
import unittest
from unittest import mock
import pytest
from app.LichessGameDownloader import LichessGameDownloader
from app.GameAnalysisEngine import GameAnalysisEngine

def test_get_fens(get_sample_game_info):
    game_id, pgn, expected_fens, _ = get_sample_game_info
    print(f"test_get_fens running for game_id = {game_id}")

    testEngine = GameAnalysisEngine()
    testEngine.load_game(pgn)
    assert testEngine.get_fens() == expected_fens

def test_extract_pgn_data(get_sample_game_info):
    game_id, pgn, _, expected_game_df = get_sample_game_info
    print(f"test_create_features running for game_id = {game_id}")

    testEngine = GameAnalysisEngine()
    testEngine.load_game(pgn)
    testEngine._extract_pgn_data()

    print(testEngine.game_df[['white_moves','black_moves','white_captures','black_captures']])
    
    ## we don't assert the evals because those are not completely deterministic
    ## e.g. the eval might change if the computer thinks slightly longer,
    # =# or utilizes a different amount of processing power on different systems
    
    test_game_df = testEngine.game_df[['white_moves','black_moves','white_captures','black_captures']]
    assert_frame_equal(test_game_df, expected_game_df)