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
console.log(parent_id);

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
  //if (!legalmoves.includes(move.san) && legalmoves.length > 0) {
  //  game.undo();
  //  console.log("not legal");
  //$legalmoves.html("Moves in our database include: " + String(legalmoves));
  //  return "snapback";
  //}
  //
  //valid move has been reached
  $legalmoves.html("");
  updateStatus();
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
    data: JSON.stringify({ pgn: game.pgn(), id: id }),
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

var config = {
  draggable: true,
  position: "start",
  onDragStart: onDragStart,
  onDrop: onDrop,
  onSnapEnd: onSnapEnd,
};
board = Chessboard("myBoard", config);

updateStatus();
