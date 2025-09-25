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
    print(f"test_extract_pgn_data running for game_id = {game_id}")

    testEngine = GameAnalysisEngine()
    testEngine.load_game(pgn)

    ## we should mock the eval portion of this function
    ## so that the test doesn't waste time on evaluations that we don't test?
    testEngine._extract_pgn_data()

    ## we don't assert the evals because those are not completely deterministic
    ## e.g. the eval might change if the computer thinks slightly longer,
    ## or utilizes a different amount of processing power on different systems

    test_game_df = testEngine.game_df[['white_moves','black_moves','white_captures','black_captures']]
    expected_extracted_df = expected_game_df[['white_moves','black_moves','white_captures','black_captures']]
    assert_frame_equal(test_game_df, expected_extracted_df)

def test_create_features(get_sample_game_info):
    game_id, pgn, _, expected_game_df = get_sample_game_info
    print(f"test_create_features running for game_id = {game_id}")
    testEngine = GameAnalysisEngine()
    testEngine.load_game(pgn)
    testEngine._extract_pgn_data()
    testEngine._create_features()

    test_game_df = testEngine.game_df[['white_opp_capture','black_opp_capture','white_time_spent','black_time_spent']]
    expected_feature_df = expected_game_df[['white_opp_capture','black_opp_capture','white_time_spent','black_time_spent']]
    assert_frame_equal(test_game_df, expected_feature_df)

def test_flag_moves():
    pass