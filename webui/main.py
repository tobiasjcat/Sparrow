#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

from bottle import get, run, static_file, template
from pprint import pformat, pprint

import db_utils

@get("/favicon.ico")
def get_favicon():
    return static_file("favicon.ico", root="static")

@get("/static/<sfile>")
def get_sfile(sfile):
    return static_file(sfile, root="static")

@get("/")
@get("/index")
def mainpage():
    return template("templates/index.html")

@get("/api/tables/all_hours")
def api_get_all_hours_table():
    hdata = db_utils.get_all_hours_data()
    ttitle = "All calls for each hour of the day"
    return template("templates/tables/hours.html", hdata=hdata, ttitle=ttitle)

@get("/api/tables/danger_hours")
def api_get_all_hours_table():
    hdata = db_utils.get_danger_hours_data()
    ttitle = "Calls for violent incidents for each hour of the day"
    return template("templates/tables/hours.html", hdata=hdata, ttitle=ttitle)

def main():
    run(host="0.0.0.0", port=42133)

if __name__ == '__main__':
    exit(main())
