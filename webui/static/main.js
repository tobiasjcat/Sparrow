function load_all_hours_table() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var all_hours_div = document.getElementById("all_hours_table");
      all_hours_div.innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/api/tables/all_hours", true);
  xhttp.send();
}

function load_danger_hours_table() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var all_hours_div = document.getElementById("danger_hours_table");
      all_hours_div.innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "/api/tables/danger_hours", true);
  xhttp.send();
}

function load_all_elements() {
  load_all_hours_table();
  load_danger_hours_table();
}
