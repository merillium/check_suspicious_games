import base64
from dash import Dash, dcc, html, Input, Output, State, ctx
from LichessGameDownloader import LichessGameDownloader
from GameAnalysisEngine import GameAnalysisEngine

external_scripts = [
    "https://code.jquery.com/jquery-3.6.0.min.js",  # jQuery first
    "https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.js",  # chessboard.js next
]

external_stylesheets = [
    "https://cdnjs.cloudflare.com/ajax/libs/chessboard-js/1.0.0/chessboard-1.0.0.min.css"
]

app = Dash(
    __name__,
    external_scripts=external_scripts,
    external_stylesheets=external_stylesheets
)

app.layout = html.Div([

    ## supports pgn upload currently (must have timestamps)
    ## will also want to support API call to load game

    html.Div(id="board", style={"width": "400px"}),
    html.Br(),
    dcc.Store(id="fens-store"),  # stores the list of FENs
    dcc.Store(id="dummy"), # dummy output for clientside callback
    html.Div(
        [
            dcc.Slider(
                id="move-slider",
                className = 'slider',
                min=0,
                max=0,  # will update dynamically
                step=1,
                value=None,
            )
        ],
        style={"paddingLeft": "10px", 'width': '450'},
    ),
    
    dcc.Textarea(
        id='game-info',
        value='Enter game_id or lichess game url',
        style={'width': '60%', 'height': 30},
    ),
    html.Br(),
    dcc.Textarea(
        id='pgn-textarea',
        value='Analysis will show up here',
        readOnly=True,
        style={'width': '60%', 'height': 200},
    ),
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
    html.Div(
        id="pgn-upload-message",
        style={
            "whiteSpace": "pre-line",
            "color": "red",
            "paddingLeft": "10px",
        },
    ),
    html.Div(id='dummy-output'),
])

# @app.callback(
#     Output("pgn-textarea", "value"),
#     Output("pgn-data","data"),
#     Input("upload-pgn-data", "contents"),
#     prevent_initial_call=True,
# )
# def download_game(content):
#     pass


@app.callback(
    Output("pgn-textarea", "value", allow_duplicate=True),
    Output("pgn-upload-message", "children"),
    Output("pgn-data","data"),
    Input("upload-pgn-data", "contents"),
    State("upload-pgn-data", "filename"),
    prevent_initial_call=True,
)
def process_upload(content, filename):
    if not filename.endswith(".pgn"):
        error_message = "Error: you must upload a .pgn file"
        return "",error_message,None
    else:
        try:
            _, content_string = content.split(',', 1)
            decoded = base64.b64decode(content_string)
            pgn_string = decoded.decode('utf-8')
            return pgn_string, "Successfully loaded!", pgn_string
        except Exception as e:
            print(e)
            error_message = "Error: your pgn file could not be processed"
            return "", error_message, None

## allow duplicate output, since there's a button being pressed which is separate from loading a file
## so there cannot be a race condition...
## this is for debugging, eventually the output will be a table of moves
@app.callback(
    Output("fens-store", "data"),
    Output("move-slider", "max"),
    Input("analyze-game", "n_clicks"),
    State("upload-pgn-data", "contents"),
    State("pgn-data","data"),
    prevent_initial_call=True,
)
def analyze_game(n_clicks, content, pgn_data):
    try:
        print("analyzing game...")
        testEngine = GameAnalysisEngine()
        testEngine.load_game(pgn_data)
        
        ## doesn't actually analyze game yet!
        ## get the slider bar working
        # testEngine.analyze_game()

        fens = testEngine.get_fens()
        return fens, len(fens)-1
    except Exception as e:
        error_message = f"Error: your pgn file could not be analyzed due to {e}"
        return error_message, 0

## clientside callback to update the board based on the position of the slider
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
    Input("move-slider", "value"),
    State("fens-store", "data"),
    prevent_initial_call=True,
)

if __name__ == '__main__':
    app.run(debug=True)