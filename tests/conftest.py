import textwrap
import pytest

GAME_ID_TO_PGN = {
    'aLP7JnzH': """
            [Event "rated blitz game"]
            [Site "https://lichess.org/aLP7JnzH"]
            [Date "2025.08.14"]
            [White "joddle"]
            [Black "leonxjt"]
            [Result "0-1"]
            [GameId "aLP7JnzH"]
            [UTCDate "2025.08.14"]
            [UTCTime "01:14:00"]
            [WhiteElo "2581"]
            [BlackElo "2580"]
            [WhiteRatingDiff "-6"]
            [BlackRatingDiff "+6"]
            [Variant "Standard"]
            [TimeControl "180+2"]
            [ECO "D11"]
            [Opening "Slav Defense: Quiet Variation"]
            [Termination "Normal"]
            [Annotator "lichess.org"]

            1. d4 d5 2. c4 c6 3. Nf3 Nf6 4. e3 { D11 Slav Defense: Quiet Variation } e6 5. b3 Nbd7 6. Bb2 Ne4 7. Bd3 Bb4+ 8. Nbd2 f5 9. O-O O-O 10. a3 Bd6 11. Ne5 Nxe5 12. dxe5 Be7 13. Nf3 Nc5 14. Be2 dxc4 15. Bxc4? { (-0.05 → -1.28) Mistake. bxc4 was best. } (15. bxc4) 15... Qxd1 16. Raxd1 b5 17. Bd3 Nxb3 18. Bc2 Na5 19. Nd4 c5 20. Nxb5 Rb8 21. a4 a6 22. Bc3 axb5 23. Bxa5 Ra8 24. Bc7 bxa4 25. e4 Ba6 26. Rfe1 Bc4 27. exf5 Rxf5?? { (-2.18 → 0.07) Blunder. a3 was best. } (27... a3) 28. Bxf5 exf5 29. Bd6 Bf8 30. e6 Bxd6 31. Rxd6 a3 32. e7 Re8 33. Rc6 a2 34. Rxc5 Rxe7 35. Rc8+ Kf7 36. Rxe7+?? { (-0.10 → -4.95) Blunder. Ra1 was best. } (36. Ra1) 36... Kxe7 37. Ra8 Kd6 38. f4?! { (-4.39 → -5.61) Inaccuracy. Rd8+ was best. } (38. Rd8+ Kc5 39. Rd1 Bd3 40. Ra1 Bb1 41. h4 Kb4 42. Kh2 Kb3 43. Kg3 Kb2) 38... Kc5 39. Kf2 Kb4 40. Ke3 Kc3 { White resigns. } 0-1""",
    'XXXXXXX-': None,
    'MnLpAAgm': """
            [Event "rated blitz game"]
            [Site "https://lichess.org/MnLpAAgm"]
            [Date "2025.08.25"]
            [White "SolidMemoryChess"]
            [Black "joddle"]
            [Result "0-1"]
            [GameId "MnLpAAgm"]
            [UTCDate "2025.08.25"]
            [UTCTime "01:56:20"]
            [WhiteElo "2454"]
            [BlackElo "2597"]
            [WhiteRatingDiff "-4"]
            [BlackRatingDiff "+4"]
            [Variant "Standard"]
            [TimeControl "180+0"]
            [ECO "C69"]
            [Opening "Ruy Lopez: Exchange Variation, Alapin Gambit"]
            [Termination "Normal"]
            [Annotator "lichess.org"]

            1. e4 e5 2. Nf3 Nc6 3. Bb5 a6 4. Bxc6 dxc6 5. O-O Bg4 6. h3 h5 { C69 Ruy Lopez: Exchange Variation, Alapin Gambit } 7. d3 Qf6 8. Be3 Bxf3 9. Qxf3 Qxf3 10. gxf3 Bd6 11. Nd2 Ne7 12. Rfb1 c5 13. Kf1 f5 14. Nc4 b5 15. Nxd6+ cxd6 16. Ke2? { (-0.17 → -1.83) Mistake. f4 was best. } (16. f4) 16... f4 17. Bd2 Kf7 18. Rg1?! { (-1.13 → -1.93) Inaccuracy. b4 was best. } (18. b4 Nc6 19. bxc5 dxc5 20. Bc3 b4 21. Bb2 a5 22. Rg1 Kf6 23. h4 a4) 18... Ng6?! { (-1.93 → -0.81) Inaccuracy. Nc6 was best. } (18... Nc6 19. c3 a5 20. a3 g6 21. h4 Rhb8 22. Rgd1 a4 23. Rab1 Ra6 24. Rg1) 19. Rg5? { (-0.81 → -2.12) Mistake. b4 was best. } (19. b4 cxb4) 19... Nh4?? { (-2.12 → -0.38) Blunder. Nf8 was best. } (19... Nf8) 20. Rag1?! { (-0.38 → -0.95) Inaccuracy. b4 was best. } (20. b4) 20... g6 21. Ra1 Kf6 22. Rgg1 g5 23. c3 a5 24. a4 b4 25. cxb4?! { (-1.78 → -2.46) Inaccuracy. Rad1 was best. } (25. Rad1 Ng6 26. Rg2 Rhg8 27. Rb1 Ra7 28. Rh1 bxc3 29. Bxc3 Nh4 30. Rgg1 Rb7) 25... axb4 26. b3 Ng6 27. Bc1 Ne7 28. Bb2 Nc6 29. Kd2 Na5 30. Kc2 Rag8 31. Rg2 Rg6? { (-3.42 → -1.62) Mistake. g4 was best. } (31... g4 32. hxg4 hxg4 33. fxg4 Kg5 34. Rc1 Rh3 35. Re1 Rgh8 36. Bc1 Rh2 37. Reg1) 32. Rag1 Rhg8 33. Ba1 Nc6 34. Bb2 Ke6 35. Kb1 d5 36. Rc1 Kd6 37. exd5 Kxd5 38. Rc4 g4 39. hxg4 hxg4 40. fxg4?! { (-1.29 → -2.04) Inaccuracy. Rg1 was best. } (40. Rg1 Nb8) 40... Rxg4 41. Rh2?? { (-1.75 → -3.90) Blunder. Rxg4 was best. } (41. Rxg4) 41... Rg1+ 42. Ka2 R1g2 43. Rh7?! { (-3.51 → -5.11) Inaccuracy. Rxg2 was best. } (43. Rxg2 Rxg2 44. Rc2 Rg1 45. Re2 Kd6 46. a5 Rg7 47. Kb1 Ra7 48. Re1 Rxa5) 43... Rxf2 44. Rd7+?! { (-5.00 → -7.13) Inaccuracy. Rc1 was best. } (44. Rc1 Rgg2 45. Rb1 Rc2 46. Rd7+ Ke6 47. Rc7 Kd6 48. Rh7 Rcd2 49. Ka1 Na5) 44... Ke6 45. Rh7 Rgg2 { White resigns. } 0-1""",
}

@pytest.fixture(params=['aLP7JnzH','XXXXXXX-','MnLpAAgm'])
def get_sample_pgn(request):
    """Return sample PGN string based on game code"""
    return textwrap.dedent(GAME_ID_TO_PGN[request.param]).strip()