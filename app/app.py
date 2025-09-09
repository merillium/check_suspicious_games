import base64
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, ctx, no_update, dash_table
import dash_bootstrap_components as dbc
from LichessGameDownloader import LichessGameDownloader
from GameAnalysisEngine import GameAnalysisEngine

external_scripts = [
    "https://code.jquery.com/jquery-3.6.0.min.js",  # jQuery first
    "https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js",  # chessboard.js next
]

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css",
]

app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([
    html.Div([

        html.Div(id="board"),
        html.Br(),
        dcc.Store(id="fens-store"),  # stores the list of FENs
        dcc.Store(id="move-idx", data=0),
        dcc.Store(id="dummy"), # dummy output for clientside callback
        html.Div(
            [
                html.Button('<<', id='move-beginning', className='move-button', n_clicks=0, disabled=True,),
                html.Span(" "),
                html.Button('<', id='move-back', className='move-button', n_clicks=0, disabled=True,),
                html.Span(" "),
                html.Button('>', id='move-forward', className='move-button', n_clicks=0, disabled=True),
                html.Span(" "),
                html.Button('>>', id='move-end', className='move-button', n_clicks=0, disabled=True,),
            ],
            className='all-move-buttons',
        ),
        html.Br(),
        dcc.Textarea(
            id='game-info',
            value='Enter game_id or lichess game url',
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                html.Button(
                    "Download Game",
                    id="download-game",
                    n_clicks=0,
                    style={"whiteSpace": "pre-wrap"},
                )
            ],
            style={"paddingLeft": "10px"},
        ),
        html.Br(),
        dcc.Upload(
            id="upload-pgn-data",
            children=html.Div(
                [
                    "Drag and Drop or ",
                    html.A("Select a pgn file"),
                ]
            ),
            max_size=10**6,
            style={
                "height": "60px",
                "width": "300px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
            },
        ),
        dcc.Store(id="pgn-data"),
        html.Br(),
        html.Div(
            [
                html.Button(
                    "Analyze Game",
                    id="analyze-game",
                    n_clicks=0,
                    style={"whiteSpace": "pre-wrap"},
                )
            ],
            style={"paddingLeft": "10px"},
        ),
        html.Br(),
        html.Div(id="pgn-load-message"),
        html.Div(id='dummy-output'),
    ], className='fixed'),
    html.Div([
        dcc.Loading(
            [dash_table.DataTable(
                id='analysis-table',
                data=[],
                columns=[],
                # filter_action="native", 
                style_table={'overflowX': 'auto'},
                style_cell={
                    # all three widths are needed
                    'minWidth': '50px', 'width': '180px', 'maxWidth': '180px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                }
        )],
        overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
        custom_spinner=html.Div(
            [
                html.H2("Analyzing Game..."),
                dbc.Spinner(color="danger"),
            ],
            id='custom-spinner',
            style={
                "flexDirection": "row", 
                "paddingTop": "150px",   # push down from top
                "textAlign": "center",   # center horizontally
            }
        )
        )
    ], className='flex-item')
    ## supports pgn upload currently (must have timestamps)
    ## will also want to support API call to load game
], className='container')

@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("pgn-data","data", allow_duplicate=True),
    Output("analyze-game","disabled", allow_duplicate=True),
    Input("download-game", "n_clicks"),
    Input("game-info", "value"),
    prevent_initial_call=True,
)
def download_game(download_click, game_code):
    if ctx.triggered_id == 'download-game':
        try:
            gameDownloader = LichessGameDownloader()
            gameDownloader.get_game(game_code.strip())
            pgn_data = gameDownloader.pgn
            return "Game successfully downloaded!", pgn_data, False
        except Exception as e:
            error_message = f"Error while downloading game: {e}! Please check the game code or URL"
            return error_message, None, False
    else:
        return no_update, no_update, False

@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("pgn-data","data"),
    Output("analyze-game","disabled", allow_duplicate=True),
    Input("upload-pgn-data", "contents"),
    State("upload-pgn-data", "filename"),
    prevent_initial_call=True,
)
def process_upload(content, filename):
    if not filename.endswith(".pgn"):
        error_message = "Error: you must upload a .pgn file"
        return error_message, None, no_update
    else:
        try:
            _, content_string = content.split(',', 1)
            decoded = base64.b64decode(content_string)
            pgn_string = decoded.decode('utf-8')

            ## re-enable [Analyze Game] button, if it was previously disabled
            return "Game successfully uploaded!", pgn_string, False
        except Exception as e:
            print(e)
            error_message = "Error: your pgn file could not be processed"
            return error_message, None, no_update

@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("fens-store", "data"),
    Output("move-beginning", "disabled"),
    Output("move-back", "disabled"),
    Output("move-forward", "disabled"),
    Output("move-end", "disabled"),
    Output("move-idx", "data", allow_duplicate=True),
    Output("analysis-table", "data"),
    Output("analysis-table", "columns"),
    Output("analyze-game","disabled"),
    Input("analyze-game", "n_clicks"),
    State("upload-pgn-data", "contents"),
    State("pgn-data","data"),
    State("move-idx","data"),
    prevent_initial_call=True,
)
def analyze_game(n_clicks, content, pgn_data, move_idx):
    print(f"pgn_data = {pgn_data}")
    if pgn_data is None:
        error_message = f"Error: no pgn file found"
        return error_message, None, True, True, True, True, move_idx, no_update, no_update, no_update
    try:
        print("analyzing game...")
        gameAnalysisEngine = GameAnalysisEngine()
        gameAnalysisEngine.load_game(pgn_data)

        fens = gameAnalysisEngine.get_fens()
        
        analysis_df = gameAnalysisEngine.analyze_game()

        ## convert list columns to strings so that they are json serializeable 
        for col in analysis_df.columns:
            analysis_df[col] = analysis_df[col].apply(
                lambda x: str(x) if isinstance(x, (list, dict)) else x
            )
        data = analysis_df.to_dict("records")
        columns = [{"name": i, "id": i} for i in analysis_df.columns]

        ## reenable move buttons, and disable the analyze game button
        move_idx = 0
        return "", fens, False, False, False, False, move_idx, data, columns, True
    except Exception as e:

        ## for debugging purposes, raise Exception
        raise(e)
    
        ## when deploying the app, we don't want to actually crash the app,
        ## so instead display an error message

        # error_message = f"Error: your pgn file could not be analyzed due to {e}"
        # return error_message, None, True, True, True, True, 0, no_update, no_update, no_update

@app.callback(
    Output("move-idx", "data", allow_duplicate=True),
    Output("analysis-table", "style_data_conditional"),
    Input("move-beginning", "n_clicks"),
    Input("move-back", "n_clicks"),
    Input("move-forward", "n_clicks"),
    Input("move-end", "n_clicks"),
    State("move-idx", "data"),
    State("fens-store", "data"),
    prevent_initial_call=True,
)
def make_moves(beginning_click, back_click, forward_click, end_click, move_idx, fens):
    """
    This callback handles a user moving forward or backwards in their game.
    The internal move index, javascript board, and analysis table are updated.
    """
    
    if ctx.triggered_id == 'move-beginning':
        if move_idx == 0:
            pass
        else:
            move_idx = 0
    
    elif ctx.triggered_id == 'move-back':
        if move_idx == 0:
            pass
        else:
            move_idx = move_idx - 1
    
    elif ctx.triggered_id == 'move-forward':
        if move_idx == len(fens)-1:
            pass
        else:
            move_idx = move_idx + 1
    
    elif ctx.triggered_id == 'move-end':
        if move_idx == len(fens)-1:
            pass
        else:
            move_idx = len(fens)-1
    
    else:
        return no_update, no_update
    
    row_idx = (move_idx-1) // 2

    ## reference for how to highlight rows from a callback
    ## https://community.plotly.com/t/highlighting-selected-rows/49595/5
    row_selection = [{"if": {"row_index": row_idx}, "backgroundColor": "#C2F2FF"}]

    # print(row_selection)

    return move_idx, row_selection

@app.callback(
    Output("move-idx", "data", allow_duplicate=True),
    Output("analysis-table", "style_data_conditional", allow_duplicate=True),
    Input("analysis-table", "active_cell"),
    prevent_initial_call=True,
)
def handle_data_analysis_click(active_cell):
    """
    This callback handles when the user clicks on the data analysis
    The board and internal move index is updated accordingly
    """
    if active_cell is None:
        return no_update
    
    # print(f"you selected {active_cell}")

    column_id = active_cell['column_id']
    if column_id not in ['white_moves','black_moves']:
        return no_update
    
    else:
        row_idx = active_cell['row']
        col_idx = 0 if column_id == 'white_moves' else 1
        move_idx = row_idx*2 + col_idx + 1

        # print(f"calculate move_idx = {move_idx}")

        row_selection = [{"if": {"row_index": row_idx}, "backgroundColor": "#C2F2FF"}]
        return move_idx, row_selection


## This clientside_callback helps update the board when the move index change
## It updates the javascript board using the variable fen = fens[move_idx]
app.clientside_callback(
    """
    function(move_idx, fens) {
        if (!fens || move_idx == null) {
            return window.dash_clientside.no_update;
        }
        var fen = fens[move_idx];
        window.updateBoardFen(fen);
    }
    """,
    Output("dummy", "data"),  # dummy output
    Input("move-idx", "data"),
    State("fens-store", "data"),
    prevent_initial_call=True,
)

if __name__ == '__main__':
    app.run(debug=True)