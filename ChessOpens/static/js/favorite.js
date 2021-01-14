function favorite(op_id) {
  console.log(op_id);
  req = $.ajax({
    type: "POST",
    url: "/favorite",
    data: JSON.stringify({ opening_id: op_id, current_url: "/home" }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    let name = "#favorite_button" + data.id;
    $(name).attr("onclick", "unfavorite(" + data.id + ")");
    $(name).html("");
    $(name).append(data.status);
  });
}

function unfavorite(op_id) {
  console.log(op_id);
  req = $.ajax({
    type: "POST",
    url: "/unfavorite",
    data: JSON.stringify({ opening_id: op_id, current_url: "/home" }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    let name = "#favorite_button" + data.id;
    $(name).attr("onclick", "favorite(" + data.id + ")");
    $(name).html("");
    $(name).append(data.status);
  });
}
function remove(op_id) {
  req = $.ajax({
    type: "POST",
    url: "/delete_op",
    data: JSON.stringify({ id: op_id }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function () {
    let name = "#remove_button" + op_id;
    $(name).html("");
    $(name).append("deleted");
  });
}
