import io
import numpy as np
import pandas as pd
import chess.pgn
from stockfish import Stockfish

class GameAnalysisEngine:
    """A class to parse and analyze a pgn of a chess game, adding features to help with cheat detection"""

    def __init__(self):
        self.pgn = None
        self.game = None

        ## 0.1s of thinking time is probably sufficient, but more unit tests will help
        self.engine = Stockfish(
            path='/opt/homebrew/bin/stockfish', 
            depth=18, 
            parameters={"Threads": 2, "Minimum Thinking Time": 0.1}
        )
        self.game_df = None
    
    def load_game(self, pgn):
        self.pgn = io.StringIO(pgn)
        self.game = chess.pgn.read_game(self.pgn)
    
    def _extract_pgn_data(self):
        if self.pgn is None:
            raise Exception("You must load a pgn first")
        
        white_moves = []
        # white_comments = []
        white_evals = []
        white_times = []
        white_top_moves = []

        black_moves = []
        # black_comments = []
        black_evals = []
        black_times = []
        black_top_moves = []

        #or if you want to loop over all game nodes:
        ply = 0
        while not self.game.is_end():
            node = self.game.variations[0]
            move = str(node.move)

            ## keep all evals from white's point of view
            self.engine.make_moves_from_current_position([move])
            top_moves = self.engine.get_top_moves(3)
            eval = self.engine.get_evaluation()['value'] / 100

            time = node.clock()
            # comment = node.comment
            if ply % 2 == 0:
                white_moves.append(move)
                # white_comments.append(comment)
                white_evals.append(eval)
                white_times.append(time)
                white_top_moves.append(top_moves)
            else:
                black_moves.append(move)
                # black_comments.append(comment)
                black_evals.append(eval)
                black_times.append(time)
                black_top_moves.append(top_moves)
            
            self.game = node  
            ply += 1
            
        self.game_df = pd.DataFrame({
            'white_moves': white_moves,
            'black_moves': black_moves,
            'white_times': white_times,
            'black_times': black_times,
            'white_evals': white_evals,
            'black_evals': black_evals,
            'white_top_moves': white_top_moves,
            'black_top_moves': black_top_moves,
        })
    
    def _classify_moves(self):
        """Classify moves as critical or forced
        
        We will use the following definitions for simplicity:
        (1) critical means that the evals between the best N moves differs by a lot ( > 1.00 cp)
        (2) forced means that there is only one reasonable good move (e.g. recapture, only legal move)

        """
        pass
    
    def _create_features(self):
        self.game_df['black_evals_shifted'] = self.game_df['black_evals'].shift(1)
        self.game_df['white_eval_diff'] = self.game_df['white_evals'] - self.game_df['black_evals_shifted']

        ## make this value negative so it's the change from black's perspective
        self.game_df['black_eval_diff'] = - (self.game_df['black_evals'] - self.game_df['white_evals'])

        eval_bins = [-np.inf, -1.00, -0.50, -0.20, 1.00]
        move_class = ['blunder','mistake','inaccuracy','good']

        self.game_df['white_evals_ind'] = pd.cut(self.game_df['white_eval_diff'], bins=eval_bins, labels=move_class)
        self.game_df['black_evals_ind'] = pd.cut(self.game_df['black_eval_diff'], bins=eval_bins, labels=move_class)
        print(self.game_df[['white_moves','black_moves','white_top_moves','black_top_moves']].to_string())
        
        white_avg_cp_loss = self.game_df['white_eval_diff'].sum() / len(self.game_df)
        black_avg_cp_loss = self.game_df['black_eval_diff'].sum() / len(self.game_df)
        # print(f"white average cp loss = {white_avg_cp_loss}")
        # print(f"black average cp loss = {black_avg_cp_loss}")

        self._classify_moves()
    
    def analyze_game(self):
        self._extract_pgn_data()
        self._create_features()
