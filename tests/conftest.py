import numpy as np
import pandas as pd
import textwrap
import pytest

GAME_INFO = {
    'test': {
        "pgn": """
            [Event "rated blitz game"]
            [Site "https://lichess.org/test"]
            [Date "2999.12.31"]
            [White "joddle"]
            [Black "testJoddle"]
            [Result "1/2-1/2"]
            [GameId "xxxxxX"]
            [UTCDate "2999.12.31"]
            [UTCTime "11:11:11"]
            [WhiteElo "2100"]
            [BlackElo "2000"]
            [WhiteRatingDiff "-2"]
            [BlackRatingDiff "+2"]
            [Variant "Standard"]
            [TimeControl "180+2"]
            [ECO ""]
            [Opening ""]
            [Termination ""]
            [Annotator "lichess.org"]

            1. d4 { [%clk 0:03:00] } d6 { [%clk 0:03:00] } 
            2. c4 { [%clk 0:02:59] } e5 { [%clk 0:02:59] } 
            3. dxe5 { [%clk 0:02:58] } dxe5 { [%clk 0:02:58] }
            4. Qxd8+ { [%clk 0:02:58] } Kxd8 { [%clk 0:02:00] }  
            5. Nc3 { [%clk 0:02:50] } 
            { Draw Agreed. } 1/2-1/2
        """,
       "expected_fens": [
           'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', # starting position
           'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/ppp1pppp/3p4/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 0 2', 
           'rnbqkbnr/ppp1pppp/3p4/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', 'rnbqkbnr/ppp2ppp/3p4/4p3/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3', 
           'rnbqkbnr/ppp2ppp/3p4/4P3/2P5/8/PP2PPPP/RNBQKBNR b KQkq - 0 3', 'rnbqkbnr/ppp2ppp/8/4p3/2P5/8/PP2PPPP/RNBQKBNR w KQkq - 0 4', 
           'rnbQkbnr/ppp2ppp/8/4p3/2P5/8/PP2PPPP/RNB1KBNR b KQkq - 0 4', 'rnbk1bnr/ppp2ppp/8/4p3/2P5/8/PP2PPPP/RNB1KBNR w KQ - 0 5', 
           'rnbk1bnr/ppp2ppp/8/4p3/2P5/2N5/PP2PPPP/R1B1KBNR b KQ - 1 5' # white makes a move, draw agreed
        ],
        "expected_game_df": pd.DataFrame({
            'white_moves': ['d2d4','c2c4','d4e5','d1d8','b1c3'],
            'black_moves': ['d7d6','e7e5','d6e5','e8d8',np.nan],
            'white_captures': [False, False, True, True, False],
            'black_captures': [False, False, True, True, np.nan],
            'white_opp_capture': [None, False, False, True, True],
            'black_opp_capture': [False, False, True, True, False],
            'white_time_spent': [np.nan, 3.0, 3.0, 2.0, 10.0],
            'black_time_spent': [np.nan, 3.0, 3.0, 60.0, np.nan],
        })
    },
}

@pytest.fixture(params=['test'])
def get_sample_game_info(request):
    """Return sample PGN string based on game code"""
    test_game_info = GAME_INFO[request.param]
    return request.param, textwrap.dedent(test_game_info["pgn"]).strip(), test_game_info["expected_fens"], test_game_info["expected_game_df"]