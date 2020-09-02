function load_all_hours_table() {
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      console.log(this.responseText);
    }
  };
  xhttp.open("GET", "/api/tables/all_hours", true);
  xhttp.send();
}

function load_danger_hours_table() {
  null;
}

function load_all_elements() {
  load_all_hours_table();
}
