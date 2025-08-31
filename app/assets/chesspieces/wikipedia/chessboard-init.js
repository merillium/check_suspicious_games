function initChessboard() {
    const node = document.getElementById("board");
    if (!node) {
        // retry in 50ms if the div isn’t rendered yet
        setTimeout(initChessboard, 50);
        return;
    }

    window.board = Chessboard(node, {
        position: 'start',
        showNotation: false,
        pieceTheme: '/assets/chesspieces/wikipedia/{piece}.png'
    });
}

// start initialization immediately
initChessboard();

// helper function to update FEN
window.updateBoardFen = function(fen) {
    if (!window.board) {
        console.warn("Board not ready yet!");
        return;
    }
    window.board.position(fen);
    console.log("Board updated to FEN:", fen);
};