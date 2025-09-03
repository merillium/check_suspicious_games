import io
import numpy as np
import pandas as pd
import chess
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
    
    def load_game(self, pgn: str):
        if not isinstance(pgn, str):
            raise TypeError(f"pgn must be of type string, got {type(pgn)} instead")
        self.pgn = io.StringIO(pgn)
        self.game = chess.pgn.read_game(self.pgn)
    
    def get_fens(self):
        if self.pgn is None:
            raise Exception("You must load a pgn first")
        
        board = chess.Board()
        fens = [board.starting_fen]
        
        node = self.game
        while not node.is_end():
            move = str(node.variations[0].move)
            board.push_uci(move)
            fens.append(board.fen())
            node = node.variations[0]
                    
        return fens
    
    def _extract_pgn_data(self):
        if self.pgn is None:
            raise Exception("You must load a pgn first")
        
        white_moves = []
        white_evals = []
        white_times = []
        white_top_moves = []
        white_top_evals = []

        black_moves = []
        black_evals = []
        black_times = []
        black_top_moves = []
        black_top_evals = []

        #or if you want to loop over all game nodes:
        ply = 0
        while not self.game.is_end():
            node = self.game.variations[0]
            move = str(node.move)

            ## keep all evals from white's point of view
            self.engine.make_moves_from_current_position([move])
            top_moves_info = self.engine.get_top_moves(5)
            top_moves = [info['Move'] for info in top_moves_info]
            top_evals = [info['Centipawn']/100 for info in top_moves_info]

            eval = self.engine.get_evaluation()['value'] / 100

            time = node.clock()
            if ply % 2 == 0:
                white_moves.append(move)
                white_evals.append(eval)
                white_times.append(time)
                white_top_moves.append(top_moves)
                white_top_evals.append(top_evals)
            else:
                black_moves.append(move)
                black_evals.append(eval)
                black_times.append(time)
                black_top_moves.append(top_moves)
                black_top_evals.append(top_evals)
            
            self.game = node  
            ply += 1

        # print(f"white_moves has length = {len(white_moves)}")
        # print(f"black_moves has length = {len(black_moves)}")
        # print(f"white_times has length = {len(white_times)}")
        # print(f"black_times has length = {len(black_times)}")

        data_dict = {
            'white_moves': white_moves,
            'black_moves': black_moves,
            'white_times': white_times,
            'black_times': black_times,
            'white_evals': white_evals,
            'black_evals': black_evals,
            'white_top_moves': white_top_moves,
            'black_top_moves': black_top_moves,
            'white_top_evals': white_top_evals,
            'black_top_evals': black_top_evals,
        }
        
        ## one liner that guarantees all columns have the same length
        self.game_df = pd.DataFrame({key:pd.Series(value) for key, value in data_dict.items()})
        print(self.game_df)
    
    @staticmethod
    def _label_moves(top_evals: list, forced_eval_th, critical_eval_spread_th, time_spent_th=None):
        if not isinstance(top_evals, list):
            return None
        
        ## only legal move --> forced
        elif len(top_evals) == 1:
            return "forced"
        
        ## the best move is much better than all other moves --> forced
        elif top_evals[0] - top_evals[1] > forced_eval_th:
            return "forced"
    
        ## out of the top 5 moves, the spread between best and worst is sufficiently large --> critical
        elif top_evals[-1] - top_evals[0] > critical_eval_spread_th:
            return "critical"
        
        ## no other classification --> ""
        else:
            return ""
    
    def _flag_moves(self, forced_eval_th=2.00, critical_eval_spread_th=2.00):
        """Flag certain moves based on critical or forced labels, combined with time spent to flag a move as suspicious
        
        We will use the following definitions for simplicity:
        (1) forced means that there is only one legal move, or the difference between the best move and second best move is greater than some threshold

        """

        self.game_df['white_top_eval_range'] = self.game_df['white_top_evals'].apply(lambda x: max(x)-min(x) if isinstance(x, list) else None)
        self.game_df['black_top_eval_range'] = self.game_df['black_top_evals'].apply(lambda x: max(x)-min(x) if isinstance(x, list) else None)

        self.game_df['white_move_class'] = self.game_df['white_top_evals'].apply(lambda x: self._label_moves(x, forced_eval_th, critical_eval_spread_th))
        self.game_df['black_move_class'] = self.game_df['black_top_evals'].apply(lambda x: self._label_moves(x, forced_eval_th, critical_eval_spread_th))
    
    def _create_features(self):
        self.game_df['black_evals_shifted'] = self.game_df['black_evals'].shift(1)
        self.game_df['white_eval_diff'] = self.game_df['white_evals'] - self.game_df['black_evals_shifted']

        ## make this value negative so it's the change from black's perspective
        self.game_df['black_eval_diff'] = - (self.game_df['black_evals'] - self.game_df['white_evals'])

        # eval_bins = [-np.inf, -1.00, -0.50, -0.20, 1.00]
        # move_class = ['blunder','mistake','inaccuracy','good']

        # self.game_df['white_evals_ind'] = pd.cut(self.game_df['white_eval_diff'], bins=eval_bins, labels=move_class)
        # self.game_df['black_evals_ind'] = pd.cut(self.game_df['black_eval_diff'], bins=eval_bins, labels=move_class)
        
        # white_avg_cp_loss = self.game_df['white_eval_diff'].sum() / len(self.game_df)
        # black_avg_cp_loss = self.game_df['black_eval_diff'].sum() / len(self.game_df)

        self._flag_moves()
        
        # print(f"white average cp loss = {white_avg_cp_loss}")
        # print(f"black average cp loss = {black_avg_cp_loss}")
    
    def analyze_game(self):
        self._extract_pgn_data()
        self._create_features()

        # print(self.game_df[['white_moves','black_moves','white_move_class','black_move_class']].to_string())

        return self.game_df[['white_moves','black_moves','white_move_class','black_move_class']]
