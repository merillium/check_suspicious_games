import lichess.api
from lichess.format import SINGLE_PGN

class LichessGameDownloader:
    """A class that uses the lichess API to download a single game, using either url or game code"""

    def __init__(self):
        self.game_url = None
        self.game_code = None
        self.pgn = None
    
    def get_game(self, game_code):
        try:
            self.pgn = lichess.api.game(game_code, format=SINGLE_PGN)
        except Exception as e:
            raise Exception(e)