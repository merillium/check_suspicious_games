import re
import lichess.api
from lichess.format import PGN

class LichessGameDownloader:
    """A class that uses the lichess API to download a single game, using either url or game code"""

    def __init__(self):
        self.game_code = None
        self.pgn = None
    
    def get_game(self, game_id):
        """Use lichess API to retrieve the pgn for a game based on the game code"""

        try:
            ## if game_code is a url, extract the game_code portion only
            if "lichess.org" in game_id:
                game_code = re.search(r"lichess\.org/([^/]+)/", game_id)
            
            else:
                ## throw an error if the game code itself is invalid
                if not game_code.isalnum():
                    raise ValueError(f"Invalid game code: {game_id}. Must be alphanumeric")
            
            final_game_code = game_id
            
            self.pgn = lichess.api.game(final_game_code, format=PGN)
        except ValueError as e:
            raise e