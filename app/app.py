from dash import Dash, dcc, html, Input, Output, State, ctx

app = Dash()

app.layout = html.Div([

    ## supports manually entered text or uploads for pgn

    dcc.Textarea(
        id='pgn-textarea',
        value='Enter pgn here',
        style={'width': '60%', 'height': 300},
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
    html.Br(),
    html.Div(
        id="pgn-upload-message",
        style={
            "whiteSpace": "pre-line",
            "color": "red",
            "padding-left": "10px",
        },
    ),
    dcc.Store(id="pgn-data"),
    html.Div(
        [
            html.Button(
                "Analyze Game",
                id="analyze-game",
                n_clicks=0,
                style={"whiteSpace": "pre-wrap"},
            )
        ],
        style={"padding-left": "10px"},
    ),
    html.Br(),
    html.Div(
        id="error-output",
        style={
            "whiteSpace": "pre-line",
            "color": "red",
            "padding-left": "10px",
        },
    ),
])

@app.callback(
    Output("pgn-textarea", "value"),
    Output("pgn-upload-message", "children"),
    Output("error-output", "children"),
    Input("analyze-game", "n_clicks"),
    State("pgn-textarea", "value"),
    State("upload-pgn-data", "filename"),
    State("upload-pgn-data", "contents"),
    prevent_initial_call=True,
)
def update_output(analyze_nclicks, pgn_string, pgn_filename, pgn_content):
    if ctx.triggered_id == "analyze-game":
        return "", "analysis not currently supported!", ""
    else:
        print(pgn_filename)
        if not pgn_filename.endswith(".pgn"):
            error_message = "Error: you must upload a .pgn file"
            return "", "", error_message

if __name__ == '__main__':
    app.run(debug=True)