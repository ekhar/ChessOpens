function undomoveBoard() {
  if (id > 1) {
    game.undo();
    id = parent_id;
    updateStatus();
    fen = game.fen();
    board.position(fen);
    updateStatus();
  }
}

function loadboard(op_id, op_pgn) {
  id = op_id;
  pgn = op_pgn;
  updateStatus();
  game.load_pgn(pgn);
  fen = game.fen();

  board.position(fen);
  updateStatus();
}
