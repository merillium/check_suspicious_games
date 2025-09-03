import base64
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, State, ctx, no_update
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
            [dcc.Graph(id='analysis', figure=go.Figure())],
            overlay_style={"visibility":"visible", "opacity": .5, "backgroundColor": "white"},
            custom_spinner=html.H2(["Analyzing Game...", dbc.Spinner(color="danger")]),
        )
    ], className='flex-item')
    ## supports pgn upload currently (must have timestamps)
    ## will also want to support API call to load game
], className='container')

@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("pgn-data","data", allow_duplicate=True),
    Input("download-game", "n_clicks"),
    Input("game-info", "value"),
    prevent_initial_call=True,
)
def download_game(download_click, game_code):
    if ctx.triggered_id == 'download-game':
        try:
            print("here")
            gameDownloader = LichessGameDownloader()
            gameDownloader.get_game(game_code.strip())
            pgn_data = gameDownloader.pgn
            return "Game successfully downloaded!", pgn_data
        except Exception as e:
            error_message = f"Error while downloading game! Please check the game code or URL"
            return error_message, None
    else:
        return no_update

@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("pgn-data","data"),
    Input("upload-pgn-data", "contents"),
    State("upload-pgn-data", "filename"),
    prevent_initial_call=True,
)
def process_upload(content, filename):
    if not filename.endswith(".pgn"):
        error_message = "Error: you must upload a .pgn file"
        return error_message,None
    else:
        try:
            _, content_string = content.split(',', 1)
            decoded = base64.b64decode(content_string)
            pgn_string = decoded.decode('utf-8')
            return "Game successfully uploaded!", pgn_string
        except Exception as e:
            print(e)
            error_message = "Error: your pgn file could not be processed"
            return error_message, None

## allow duplicate output, since there's a button being pressed which is separate from loading a file
## so there cannot be a race condition...
## this is for debugging, eventually the output will be a table of moves
@app.callback(
    Output("pgn-load-message", "children", allow_duplicate=True),
    Output("fens-store", "data"),
    Output("move-beginning", "disabled"),
    Output("move-back", "disabled"),
    Output("move-forward", "disabled"),
    Output("move-end", "disabled"),
    Output("move-idx", "data", allow_duplicate=True),
    Output("analysis", "figure"),
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
        return error_message, None, True, True, True, True, move_idx, no_update
    try:
        print("analyzing game...")
        gameAnalysisEngine = GameAnalysisEngine()
        gameAnalysisEngine.load_game(pgn_data)

        fens = gameAnalysisEngine.get_fens()
        
        ## doesn't actually analyze game yet!
        analysis_df = gameAnalysisEngine.analyze_game()
        fig = go.Figure(data=[
            go.Table(
            header=dict(values=analysis_df.columns),
            cells=dict(values=analysis_df.to_numpy().T))
        ])

        ## reenable buttons!
        print(f"storing fens: {fens}")
        move_idx = 0
        return "", fens, False, False, False, False, move_idx, fig
    except Exception as e:
        error_message = f"Error: your pgn file could not be analyzed due to {e}"
        return error_message, None, True, True, True, True, 0, no_update

@app.callback(
    Output("move-idx", "data", allow_duplicate=True),
    Input("move-beginning", "n_clicks"),
    Input("move-back", "n_clicks"),
    Input("move-forward", "n_clicks"),
    Input("move-end", "n_clicks"),
    State("move-idx", "data"),
    State("fens-store", "data"),
    prevent_initial_call=True,
)
def make_moves(beginning_click, back_click, forward_click, end_click, move_idx, fens):
    # print(f"{ctx.triggered_id} triggered")
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
        return no_update
    
    # print(f"{ctx.triggered_id} was triggered, move_idx updated to {move_idx}")
    return move_idx


## clientside callback to update the board based on the value of move-idx
## we store a list of FENs corresponding to positions in dcc.Store component, fens-store
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