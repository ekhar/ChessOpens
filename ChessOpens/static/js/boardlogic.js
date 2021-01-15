function undomoveBoard() {
  if (id > 1) {
    game.undo();
    fen = game.fen();
    board.position(fen);
    updateStatus();
    req = $.ajax({
      type: "POST",
      url: "/undo",
      data: JSON.stringify({ pgn: game.pgn(), fen: fen }),
      contentType: "application/json",
    });

    req.done(function (data) {
      $name.html(data.op_name);
      id = data.id;
      parent_id = data.parent_id;
      legalmoves = data.db_moves;
      $legalmoves.html(String(legalmoves));
    });
    $status.html(status);
    $fen.html(game.fen());
    $pgn.html(game.pgn());
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
