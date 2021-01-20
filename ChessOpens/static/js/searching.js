function searchbar(str) {
  counter = 0;
  req = $.ajax({
    type: "POST",
    url: "/search",
    data: JSON.stringify({ str_name: str }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#op_list").html("");
    $("#op_list").append(data.data);
  });
}

function view_favorites() {
  req = $.ajax({
    type: "POST",
    url: "/view_favorites",
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#op_list").html("");
    $("#op_list").append(data.data);
  });
}

function view_all() {
  //  req = $.ajax({
  //    type: "POST",
  //    url: "/view_all",
  //    contentType: "application/json",
  //  });
  //  req.done(function (data) {
  //    $("#op_list").html("");
  //    $("#op_list").append(data.data);
  //  });
}

function view_customs() {
  counter = 0;
  req = $.ajax({
    type: "POST",
    url: "/view_custom",
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#op_list").html("");
    $("#op_list").append(data.data);
  });
}
