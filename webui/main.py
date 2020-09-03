#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

from bottle import get, run, static_file, template
from pprint import pformat, pprint

import db_utils

DAYMAPPING = { \
    0:"Mon", \
    1:"Tue", \
    2:"Wed", \
    3:"Thu", \
    4:"Fri", \
    5:"Sat", \
    6:"Sun", \
}

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
    # if not red_factor:
    #     return
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
def api_get_danger_hours_table():
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


@get("/api/tables/all_weekdays")
def api_get_all_weekdays_table():
    ttitle = "All calls for each days of the week"
    hdata = db_utils.get_all_weekdays_data()
    total_incidents = sum(hdata.values())
    retval = {}
    for k in hdata:
        retval[k] = {"value" : round((hdata[k]/total_incidents) * 100, 2)}
    minval, maxval = min(retval.values(), key=lambda x:x["value"]), max(retval.values(), key=lambda x:x["value"])
    minval, maxval = minval["value"], maxval["value"]
    for k in hdata:
        retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, 0)
    return template("templates/tables/days.html", hdata=retval, ttitle=ttitle, daymap=DAYMAPPING)

@get("/api/tables/danger_weekdays")
def api_get_danger_weekdays_table100():
    ttitle = "Calls for violent incidents for each day of the week"
    hdata = db_utils.get_danger_weekdays_data()
    total_incidents = sum(hdata.values())
    retval = {}
    for k in hdata:
        retval[k] = {"value" : round((hdata[k]/total_incidents) * 100, 2)}
    minval, maxval = min(retval.values(), key=lambda x:x["value"]), max(retval.values(), key=lambda x:x["value"])
    minval, maxval = minval["value"], maxval["value"]
    for k in hdata:
        # retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, minval)
        retval[k]["bgcolor"] = hexrgb(retval[k]["value"], maxval, 0)
    return template("templates/tables/days.html", hdata=retval, ttitle=ttitle, daymap=DAYMAPPING)

@get("/api/tables/all_hourweek")
def api_get_all_hourweek_table():
    ttitle = "All calls for each hour of the week as a percentage of maximum calls"
    hdata = db_utils.get_all_hourweek_data()
    retval = {d:{h:{} for h in range(24)} for d in range(7)}
    value_list = []
    for d in range(7):
        for h in range(24):
            value_list.append(hdata[d][h])
    total_incidents = sum(value_list)
    minval, maxval = min(value_list), max(value_list)
    for d in range(7):
        for h in range(24):
            retval[d][h]["value"] = round((hdata[d][h] / maxval) * 100, 2)
            retval[d][h]["bgcolor"] = hexrgb(retval[d][h]["value"], 100, 0)

    return template("templates/tables/hour_ot_week.html", hdata=retval, ttitle=ttitle, daymap=DAYMAPPING)

@get("/api/tables/danger_hourweek")
def api_get_danger_hourweek_table():
    ttitle = "Calls for violent incidents for each hour of the week as a percentage of maximum calls"
    hdata = db_utils.get_danger_hourweek_data()
    retval = {d:{h:{} for h in range(24)} for d in range(7)}
    value_list = []
    for d in range(7):
        for h in range(24):
            value_list.append(hdata[d][h])
    total_incidents = sum(value_list)
    minval, maxval = min(value_list), max(value_list)
    for d in range(7):
        for h in range(24):
            retval[d][h]["value"] = round((hdata[d][h] / maxval) * 100, 2)
            retval[d][h]["bgcolor"] = hexrgb(retval[d][h]["value"], 100, 0)
    return template("templates/tables/hour_ot_week.html", hdata=retval, ttitle=ttitle, daymap=DAYMAPPING)


@get("/api/tables/all_quadrants")
def api_get_all_quadrants_table():
    ttitle = "Quadrants where calls originate"
    hdata = db_utils.get_all_quadrants()
    retval = {x:{y:{} for y in range(53, 112)} for x in range(25, 78)}
    value_list = []
    for x in range(25,78):
        for y in range(53,112):
            value_list.append(hdata[x][y])
    total_incidents = sum(value_list)
    minval, maxval = min(value_list), max(value_list)
    for x in range(25, 78):
        for y in range(53, 112):
            retval[x][y]["value"] = round((hdata[x][y] / maxval) * 100, 2)
            # retval[x][y]["value"] = hdata[x][y]
            retval[x][y]["bgcolor"] = hexrgb(retval[x][y]["value"], 100, 0)
    return template("templates/tables/coordinates.html", hdata=retval, ttitle=ttitle)

@get("/api/tables/non_larceny_quadrants")
def api_get_nl_quadrants_table():
    ttitle = "Quadrants where calls reporting non-larceny offenses originate"
    hdata = db_utils.get_nl_quadrants()
    retval = {x:{y:{} for y in range(53, 112)} for x in range(25, 78)}
    value_list = []
    for x in range(25,78):
        for y in range(53,112):
            value_list.append(hdata[x][y])
    total_incidents = sum(value_list)
    minval, maxval = min(value_list), max(value_list)
    for x in range(25, 78):
        for y in range(53, 112):
            retval[x][y]["value"] = round((hdata[x][y] / maxval) * 100, 2)
            # retval[x][y]["value"] = hdata[x][y]
            retval[x][y]["bgcolor"] = hexrgb(retval[x][y]["value"], 100, 0)
    return template("templates/tables/coordinates.html", hdata=retval, ttitle=ttitle)

def main():
    run(host="0.0.0.0", port=42133)

if __name__ == '__main__':
    exit(main())
