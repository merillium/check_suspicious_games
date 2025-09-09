import textwrap
import pytest

GAME_ID_TO_PGN = {
    'doCFjU1j': """
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
    'XXXXXXX-': None,
    'test': """
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

    1. d4 { [%clk 0:03:00] } 1... d5 { [%clk 0:03:00] } 2. c4 { [%clk 0:03:00] } { Black resigns. } 1-0
    """
}

@pytest.fixture(params=['doCFjU1j'])
def get_sample_pgn(request):
    """Return sample PGN string based on game code"""
    sample_pgn = GAME_ID_TO_PGN[request.param]
    return textwrap.dedent(sample_pgn).strip()