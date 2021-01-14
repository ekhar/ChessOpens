function create_opening(name) {
  var a = "";
  req = $.ajax({
    type: "POST",
    url: "/create_op",
    data: JSON.stringify({
      name: name,
      pgn: game.pgn(),
      current_url: "/create",
    }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    a = data.status;
    console.log(a);
    alert("Opening - " + name + a);
  });
}
