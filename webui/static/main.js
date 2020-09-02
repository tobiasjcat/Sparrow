function load_general_table(inurl, inelemid){
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function () {
    if (this.readyState == 4 && this.status == 200) {
      var all_hours_div = document.getElementById(inelemid);
      all_hours_div.innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", inurl, true);
  xhttp.send();
}

function load_all_elements() {
  load_general_table("/api/tables/all_hours", "all_hours_table");
  load_general_table("/api/tables/danger_hours", "danger_hours_table");
  load_general_table("/api/tables/all_weekdays", "all_weekdays_table");
  load_general_table("/api/tables/danger_weekdays", "danger_weekdays_table");
}
