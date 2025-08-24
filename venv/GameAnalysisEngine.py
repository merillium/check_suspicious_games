import pandas as pd
import chess
from stockfish import Stockfish

class GameAnalysisEngine:
    """A class to parse and analyze a pgn of a chess game, adding features to help with cheat detection"""

    def __init__(self):
        self.pgn = None
        self.engine = Stockfish(path=None)
        self.game_data = pd.DataFrame()
    
    def load_pgn(self, pgn):
        self.pgn = pgn
    
    def analyze_game(self):
        if self.pgn is None:
            raise Exception("You must load a pgn first")
        
        