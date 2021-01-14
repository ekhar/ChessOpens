var board = null;
var game = new Chess();
var $status = $("#status");
var $fen = $("#fen");
var $pgn = $("#pgn");
var $name = $("#name");
var legalmoves = op_data.legalmoves;
var $legalmoves = $("#legalmoves");
var id = op_data.id;
var parent_id = op_data.parent_id;
var player_color = "w";
var computer_move;
var playing_random = false;

var base_id = id;
var base_pgn;

function onDragStart(source, piece, position, orientation) {
  // do not pick up pieces if the game is over
  if (game.game_over()) return false;

  // only pick up pieces for the side to move
  if (
    (game.turn() === "w" && piece.search(/^b/) !== -1) ||
    (game.turn() === "b" && piece.search(/^w/) !== -1)
  ) {
    return false;
  }
}
function makeRandomMove() {
  var possibleMoves = legalmoves;

  // game over
  if (possibleMoves.length === 0 || !playing_random) return;

  var randomIdx = Math.floor(Math.random() * possibleMoves.length);
  game.move(possibleMoves[randomIdx]);
  board.position(game.fen());
  updateStatus();
}

function onDrop(source, target) {
  // see if the move is legal
  var move = game.move({
    from: source,
    to: target,
    promotion: "q", // NOTE: always promote to a queen for example simplicity
  });

  // illegal move
  if (move === null) return "snapback";
  //-----------------------FOR RANDOM PLAY----------------------------------
  //compares move to allowed moves in the position
  if (!legalmoves.includes(move.san) && playing_random) {
    //&& legalmoves.length > 0) {
    game.undo();
    return "snapback";
  }

  //valid move has been reached
  $legalmoves.html("");
  updateStatus();
  window.setTimeout(makeRandomMove, 250);
}

// update the board position after the piece snap
// for castling, en passant, pawn promotion
function onSnapEnd() {
  board.position(game.fen());
}

function updateStatus() {
  var status = "";

  var moveColor = "White";
  if (game.turn() === "b") {
    moveColor = "Black";
  }

  // checkmate?
  if (game.in_checkmate()) {
    status = "Game over, " + moveColor + " is in checkmate.";
  }

  // draw?
  else if (game.in_draw()) {
    status = "Game over, drawn position";
  }

  // game still on
  else {
    status = moveColor + " to move";

    // check?
    if (game.in_check()) {
      status += ", " + moveColor + " is in check";
    }
  }

  req = $.ajax({
    type: "POST",
    url: "/update",
    data: JSON.stringify({ pgn: game.pgn(), id: id, fen: game.fen() }),
    contentType: "application/json",
  });

  req.done(function (data) {
    $name.html(data.op_name);
    id = data.id;
    parent_id = data.parent_id;
    legalmoves = data.db_moves;
    //resetting due to completed opening
    if (legalmoves.length === 0 && playing_random) {
      legalmoves = "End of Database Moves";
      loadboard(base_id, base_pgn);
    }
    $legalmoves.html(String(legalmoves));
  });
  $status.html(status);
  $fen.html(game.fen());
  $pgn.html(game.pgn());
}

var config = {
  draggable: true,
  position: "start",
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
};

board = Chessboard("myBoard", config);
updateStatus();
