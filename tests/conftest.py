import pandas as pd
import textwrap
import pytest

GAME_INFO = {
    'doCFjU1j': {
        "pgn": """
            [Event "rated blitz game"]
            [Site "https://lichess.org/doCFjU1j"]
            [Date "2023.08.18"]
            [White "joddle"]
            [Black "landy_ing"]
            [Result "1-0"]
            [GameId "doCFjU1j"]
            [UTCDate "2023.08.18"]
            [UTCTime "02:51:49"]
            [WhiteElo "2563"]
            [BlackElo "2732"]
            [WhiteRatingDiff "+8"]
            [BlackRatingDiff "-8"]
            [Variant "Standard"]
            [TimeControl "180+2"]
            [ECO "E60"]
            [Opening "King's Indian Defense: Fianchetto Variation, Immediate Fianchetto"]
            [Termination "Time forfeit"]
            [Annotator "lichess.org"]

            1. d4 Nf6 2. c4 g6 3. g3 { E60 King's Indian Defense: Fianchetto Variation, Immediate Fianchetto } c5 4. dxc5 Bg7 5. Bg2 Qa5+ 6. Nc3 Qxc5 7. Qd3 Nc6 8. Be3 Qa5 9. Bd2 O-O 10. Nh3 d6 11. b3 Bf5 12. e4 Ne5 13. Qe2 Bg4 14. Qe3 { White wins on time. } 1-0
        """,
       "expected_fens": [
           'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1', 'rnbqkb1r/pppppppp/5n2/8/3P4/8/PPP1PPPP/RNBQKBNR w KQkq - 1 2', 'rnbqkb1r/pppppppp/5n2/8/2PP4/8/PP2PPPP/RNBQKBNR b KQkq - 0 2', 'rnbqkb1r/pppppp1p/5np1/8/2PP4/8/PP2PPPP/RNBQKBNR w KQkq - 0 3', 'rnbqkb1r/pppppp1p/5np1/8/2PP4/6P1/PP2PP1P/RNBQKBNR b KQkq - 0 3', 'rnbqkb1r/pp1ppp1p/5np1/2p5/2PP4/6P1/PP2PP1P/RNBQKBNR w KQkq - 0 4', 'rnbqkb1r/pp1ppp1p/5np1/2P5/2P5/6P1/PP2PP1P/RNBQKBNR b KQkq - 0 4', 'rnbqk2r/pp1pppbp/5np1/2P5/2P5/6P1/PP2PP1P/RNBQKBNR w KQkq - 1 5', 'rnbqk2r/pp1pppbp/5np1/2P5/2P5/6P1/PP2PPBP/RNBQK1NR b KQkq - 2 5', 'rnb1k2r/pp1pppbp/5np1/q1P5/2P5/6P1/PP2PPBP/RNBQK1NR w KQkq - 3 6', 'rnb1k2r/pp1pppbp/5np1/q1P5/2P5/2N3P1/PP2PPBP/R1BQK1NR b KQkq - 4 6', 'rnb1k2r/pp1pppbp/5np1/2q5/2P5/2N3P1/PP2PPBP/R1BQK1NR w KQkq - 0 7', 'rnb1k2r/pp1pppbp/5np1/2q5/2P5/2NQ2P1/PP2PPBP/R1B1K1NR b KQkq - 1 7', 'r1b1k2r/pp1pppbp/2n2np1/2q5/2P5/2NQ2P1/PP2PPBP/R1B1K1NR w KQkq - 2 8', 'r1b1k2r/pp1pppbp/2n2np1/2q5/2P5/2NQB1P1/PP2PPBP/R3K1NR b KQkq - 3 8', 'r1b1k2r/pp1pppbp/2n2np1/q7/2P5/2NQB1P1/PP2PPBP/R3K1NR w KQkq - 4 9', 'r1b1k2r/pp1pppbp/2n2np1/q7/2P5/2NQ2P1/PP1BPPBP/R3K1NR b KQkq - 5 9', 'r1b2rk1/pp1pppbp/2n2np1/q7/2P5/2NQ2P1/PP1BPPBP/R3K1NR w KQ - 6 10', 'r1b2rk1/pp1pppbp/2n2np1/q7/2P5/2NQ2PN/PP1BPPBP/R3K2R b KQ - 7 10', 'r1b2rk1/pp2ppbp/2np1np1/q7/2P5/2NQ2PN/PP1BPPBP/R3K2R w KQ - 0 11', 'r1b2rk1/pp2ppbp/2np1np1/q7/2P5/1PNQ2PN/P2BPPBP/R3K2R b KQ - 0 11', 'r4rk1/pp2ppbp/2np1np1/q4b2/2P5/1PNQ2PN/P2BPPBP/R3K2R w KQ - 1 12', 'r4rk1/pp2ppbp/2np1np1/q4b2/2P1P3/1PNQ2PN/P2B1PBP/R3K2R b KQ - 0 12', 'r4rk1/pp2ppbp/3p1np1/q3nb2/2P1P3/1PNQ2PN/P2B1PBP/R3K2R w KQ - 1 13', 'r4rk1/pp2ppbp/3p1np1/q3nb2/2P1P3/1PN3PN/P2BQPBP/R3K2R b KQ - 2 13', 'r4rk1/pp2ppbp/3p1np1/q3n3/2P1P1b1/1PN3PN/P2BQPBP/R3K2R w KQ - 3 14', 'r4rk1/pp2ppbp/3p1np1/q3n3/2P1P1b1/1PN1Q1PN/P2B1PBP/R3K2R b KQ - 4 14'
        ],
        "expected_game_df": pd.DataFrame({
            'white_moves': ['d2d4','c2c4','g2g3','d4c5','f1g2','b1c3','d1d3','c1e3','e3d2','g1h3','b2b3','e2e4','d3e2','e2e3'],
            'black_moves': ['g8f6','g7g6','c7c5','f8g7','d8a5','a5c5','b8c6','c5a5','e8g8','d7d6','c8f5','c6e5','f5g4',None],
        })
    },
    'test': {
        "pgn": """
            [Event "rated blitz game"]
            [Site "https://lichess.org/test"]
            [Date "2999.12.31"]
            [White "joddle"]
            [Black "testJoddle"]
            [Result "1-0"]
            [GameId "xxxxxx"]
            [UTCDate "2999.12.31"]
            [UTCTime "12:12:12"]
            [WhiteElo "2000"]
            [BlackElo "1800"]
            [WhiteRatingDiff "+2"]
            [BlackRatingDiff "-2"]
            [Variant "Standard"]
            [TimeControl "180+0"]
            [ECO "D11"]
            [Opening "Slav Defense: Test Variation"]
            [Termination "Normal"]
            [Annotator "lichess.org"]

            1. e4 { [%clk 0:03:00] } 1... c5 { [%clk 0:03:00] } 2. Nf3 { [%clk 0:03:00] } { Black resigns. } 1-0
        """,
        "expected_fens": [
            'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2', 'rnbqkbnr/pp1ppppp/8/2p5/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2',
        ],
        "expected_game_df": pd.DataFrame({
            'white_moves': ['e2e4','g1f3'],
            'black_moves': ['c7c5',None],
        })
    }
}

@pytest.fixture(params=['doCFjU1j','test'])
def get_sample_game_info(request):
    """Return sample PGN string based on game code"""
    test_game_info = GAME_INFO[request.param]
    return request.param, textwrap.dedent(test_game_info["pgn"]).strip(), test_game_info["expected_fens"], test_game_info["expected_game_df"]