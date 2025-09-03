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
            if game_id.strip() == "":
                raise ValueError(f"Invalid game code: {game_id}. Cannot be empty")
            elif "lichess.org" in game_id:

                ## match either lichess.org/{game_id} or lichess.org/{game_id}/{something else}
                final_game_code_match = re.search(r"lichess\.org/([^/]+)/?", game_id)
                final_game_code = final_game_code_match.group(1)
            
            else:
                ## throw an error if the game code itself is invalid
                if not game_id.isalnum():
                    raise ValueError(f"Invalid game code: {game_id}. Must be alphanumeric")
            
                final_game_code = game_id
            
            print(f"trying to retrieve and set pgn corresponding to game_id={final_game_code} through lichess API")
            self.pgn = lichess.api.game(final_game_code, format=PGN)
            
        except ValueError as e:
            raise e