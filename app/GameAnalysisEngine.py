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
        self.game_info = {
            'type': None,
            'time_control': None,
            'increment': None,
        }

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
        event = self.game.headers.get('Event')
        if "BLITZ" in event.upper():
            self.game_info['type'] = 'blitz'
        elif "RAPID" in event.upper():
            self.game_info['type'] = 'rapid'
        elif "CLASSICAL" in event.upper():
            self.game_info['type'] = 'classical'
        else:
            raise TypeError(f"Event of type {event} not supported!")
        
        time_control = self.game.headers.get('TimeControl')
        if time_control is None:
            raise TypeError(f"The pgn does not have a time control")
        else:
            self.game_info['time_control'] = time_control
            increment = int(time_control.split("+")[-1])
            self.game_info['increment'] = increment
    
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

        ply = 0
        while not self.game.is_end():
            node = self.game.variations[0]
            move = str(node.move)

            if move is None:
                print("Warning: move is none!")

            ## ALL evals are from white's point of view
            top_moves_info = self.engine.get_top_moves(5)
            top_moves = [info['Move'] for info in top_moves_info]
            top_evals = [info['Centipawn']/100 if info['Centipawn'] is not None else None for info in top_moves_info]

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
            
            self.engine.make_moves_from_current_position([move])
            self.game = node  
            ply += 1

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
    
    @staticmethod
    def _label_moves(top_evals: list, forced_eval_th, critical_eval_spread_th, time_spent_th=None):
        print(f"top_evals = {top_evals}")
        if (not isinstance(top_evals, list)) or (len(top_evals) == 0):
            return None
        
        ## only legal move --> forced
        elif len(top_evals) == 1:
            return "forced"
        
        ## the best move is much better than all other moves --> forced
        ## white's move [0.2, -5.00, -5.00] --> should be forced
        ## black's move [-0.2, 3.00, 4.00] --> should be forced
        elif np.abs(top_evals[0] - top_evals[1]) > forced_eval_th:
            return "forced"
    
        ## out of the top 5 moves, the spread between best and worst is sufficiently large --> critical
        ## and you can't already be losing or winning, so critical evals are only for -2.00 < best move < 2.00
        elif (top_evals[-1] - top_evals[0] > critical_eval_spread_th) & (np.abs(top_evals[0]) < 2.00):
            return "critical"
        
        ## no other classification --> ""
        else:
            return ""
    
    def _flag_moves(self, forced_eval_th=3.00, critical_eval_spread_th=2.00):
        """Flag certain moves based on critical or forced labels, combined with time spent to flag a move as suspicious
        
        We will use the following definitions for simplicity:
        (1) forced means that there is only one legal move, or the difference between the best move and second best move is greater than some threshold

        """

        # self.game_df['white_top_eval_range'] = self.game_df['white_top_evals'].apply(lambda x: max(x)-min(x) if isinstance(x, list) else None)
        # self.game_df['black_top_eval_range'] = self.game_df['black_top_evals'].apply(lambda x: max(x)-min(x) if isinstance(x, list) else None)

        self.game_df['white_move_class'] = self.game_df['white_top_evals'].apply(lambda x: self._label_moves(x, forced_eval_th, critical_eval_spread_th))
        self.game_df['black_move_class'] = self.game_df['black_top_evals'].apply(lambda x: self._label_moves(x, forced_eval_th, critical_eval_spread_th))
    
    def _create_features(self):
        # self.game_df['black_evals_shifted'] = self.game_df['black_evals'].shift(1)
        # self.game_df['white_eval_diff'] = self.game_df['white_evals'] - self.game_df['black_evals_shifted']

        ## make this value negative so it's the change from black's perspective
        # self.game_df['black_eval_diff'] = - (self.game_df['black_evals'] - self.game_df['white_evals'])

        # eval_bins = [-np.inf, -1.00, -0.50, -0.20, 1.00]
        # move_class = ['blunder','mistake','inaccuracy','good']

        # self.game_df['white_evals_ind'] = pd.cut(self.game_df['white_eval_diff'], bins=eval_bins, labels=move_class)
        # self.game_df['black_evals_ind'] = pd.cut(self.game_df['black_eval_diff'], bins=eval_bins, labels=move_class)
        
        # white_avg_cp_loss = self.game_df['white_eval_diff'].sum() / len(self.game_df)
        # black_avg_cp_loss = self.game_df['black_eval_diff'].sum() / len(self.game_df)

        ## get time spent on each move, accounting for increment!
        ## if white goes from 180s to 180s in 3+2 game, they spent 2 seconds on their move
        self.game_df['white_time_spent'] = self.game_df['white_times'].shift(1) - self.game_df['white_times'] + self.game_info['increment']
        self.game_df['black_time_spent'] = self.game_df['black_times'].shift(1) - self.game_df['black_times'] + self.game_info['increment']

        self._flag_moves()
        
        # print(f"white average cp loss = {white_avg_cp_loss}")
        # print(f"black average cp loss = {black_avg_cp_loss}")
    
    def analyze_game(self):
        self._extract_pgn_data()
        self._create_features()

        print(self.game_df[['white_moves','black_moves','white_move_class','black_move_class','white_time_spent','black_time_spent',]])
        return self.game_df[['white_moves','black_moves','white_move_class','black_move_class','white_time_spent','black_time_spent',]]
