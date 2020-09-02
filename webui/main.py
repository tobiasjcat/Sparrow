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

def hexrgb(invalue, inmax, inmin):
    red_factor = int(((invalue - inmin) / (inmax - inmin)) * 255)
    redhex = hex(red_factor + 0x100)[-2:]
    greenhex = hex((255 - red_factor) + 0x100)[-2:]
    return "#{}{}00".format(redhex, greenhex)


@get("/api/tables/all_hours")
def api_get_all_hours_table():
    ttitle = "All calls for each hour of the day"
    hdata = db_utils.get_all_hours_data()
    total_incidents = sum(hdata.values())
    retval = {}
    for k in hdata:
        retval[k] = {"value" : round((hdata[k]/total_incidents) * 100, 2)}
    minval, maxval = min(retval.values(), key=lambda x:x["value"]), max(retval.values(), key=lambda x:x["value"])
    minval, maxval = minval["value"], maxval["value"]
    for k in hdata:
        # retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, minval)
        retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, 0)
    return template("templates/tables/hours.html", hdata=retval, ttitle=ttitle)

@get("/api/tables/danger_hours")
def api_get_all_hours_table():
    ttitle = "Calls for violent incidents for each hour of the day"
    hdata = db_utils.get_danger_hours_data()
    total_incidents = sum(hdata.values())
    retval = {}
    for k in hdata:
        retval[k] = {"value" : round((hdata[k]/total_incidents) * 100, 2)}
    minval, maxval = min(retval.values(), key=lambda x:x["value"]), max(retval.values(), key=lambda x:x["value"])
    minval, maxval = minval["value"], maxval["value"]
    for k in hdata:
        # retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, minval)
        retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, 0)
    return template("templates/tables/hours.html", hdata=retval, ttitle=ttitle)

def main():
    run(host="0.0.0.0", port=42133)

if __name__ == '__main__':
    exit(main())
