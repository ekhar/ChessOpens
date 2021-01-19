var counter = 0;
function foo() {
  console.log("FOO");
}
function scroll_all() {
  if (counter === 0) {
    $("#op_list").html("");
    $("#op_list").append("<div id='sentinal'>loading</div>");
    sentinal = document.querySelector("#sentinal");
    intersectionObserver_all.observe(sentinal);
  }
  console.log("Scrolling All Called");
  req = $.ajax({
    type: "POST",
    url: "/scroll_all",
    data: JSON.stringify({ counter: counter }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#sentinal").remove();
    $("#op_list").append(data.data);
    if (!data.finished) {
      $("#op_list").append("<div id='sentinal'>loading</div>");
    }
    counter = data.counter;

    sentinal = document.querySelector("#sentinal");
    intersectionObserver_all.observe(sentinal);
  });
}

function scroll_fav() {
  if (counter === 0) {
    $("#op_list").html("");
    $("#op_list").append("<div id='sentinal_fav'>favorite_loading</div>");
    sentinal = document.querySelector("#sentinal_fav");
    intersectionObserver_fav.observe(sentinal);
  }
  console.log("Scrolling Favorite Called");
  req = $.ajax({
    type: "POST",
    url: "/scroll_fav",
    data: JSON.stringify({ counter: counter }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#sentinal").remove();
    $("#op_list").append(data.data);
    if (!data.finished) {
      $("#op_list").append("<div id='sentinal_fav'>favorite_loading</div>");
    }
    counter = data.counter;

    sentinal = document.querySelector("#sentinal_fav");
    intersectionObserver_fav.observe(sentinal);
  });
}

function scroll_created() {
  if (counter === 0) {
    $("#op_list").html("");
    $("#op_list").append("<div id='sentinal'>loading</div>");
    sentinal = document.querySelector("#sentinal_created");
    intersectionObserver_created.observe(sentinal);
  }
  console.log("Scrolling Called");
  req = $.ajax({
    type: "POST",
    url: "/scroll_created",
    data: JSON.stringify({ counter: counter }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#sentinal").remove();
    $("#op_list").append(data.data);
    if (!data.finished) {
      $("#op_list").append("<div id='sentinal_created'>loading</div>");
    }
    counter = data.counter;

    sentinal = document.querySelector("#sentinal_created");
    intersectionObserver_created.observe(sentinal);
  });
}
var searching_str = "";
function scroll_search(str) {
  searching_str = str;
  if (counter === 0) {
    $("#op_list").html("");
    $("#op_list").append("<div id='sentinal'>loading</div>");
    sentinal = document.querySelector("#sentinal");
    intersectionObserver_search.observe(sentinal);
  }
  console.log("Scrolling Called");
  req = $.ajax({
    type: "POST",
    url: "/scroll_search",
    data: JSON.stringify({ counter: counter, str_name: str }), //, op_id = opening_id, op_data, db_moves = legalmoves, id = id, parent_id=parent_id }),
    contentType: "application/json",
  });
  req.done(function (data) {
    $("#sentinal").remove();
    $("#op_list").append(data.data);
    if (!data.finished) {
      $("#op_list").append("<div id='sentinal'>loading</div>");
    }
    counter = data.counter;

    sentinal = document.querySelector("#sentinal");
    intersectionObserver_search.observe(sentinal);
  });
}

var intersectionObserver_all = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  scroll_all();
});

var intersectionObserver_fav = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  scroll_fav();
});

var intersectionObserver_created = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  scroll_created();
});
var intersectionObserver_search = new IntersectionObserver((entries) => {
  if (entries[0].intersectionRatio <= 0) {
    return;
  }
  scroll_search(searching_str);
});
// Instruct the IntersectionObserver to watch the sentinel
