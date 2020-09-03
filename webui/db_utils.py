#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

import sqlite3

conn = sqlite3.connect("stats.db")
c = conn.cursor()

def get_all_hours_data():
    return dict(c.execute("SELECT * FROM all_hour_of_the_day").fetchall())

def get_danger_hours_data():
    return dict(c.execute("SELECT * FROM danger_hour_of_the_day").fetchall())

def get_all_weekdays_data():
    return dict(c.execute("SELECT * FROM all_day_of_the_week").fetchall())

def get_danger_weekdays_data():
    return dict(c.execute("SELECT * FROM danger_day_of_the_week").fetchall())

def get_all_hourweek_data():
    db_results_list = c.execute("SELECT * FROM all_hour_of_the_week").fetchall()
    retval = {i:{} for i in range(7)}
    for d,h,r in db_results_list:
        retval[d][h] = r
    return retval

def get_danger_hourweek_data():
    db_results_list = c.execute("SELECT * FROM danger_hour_of_the_week").fetchall()
    retval = {i:{} for i in range(7)}
    for d,h,r in db_results_list:
        retval[d][h] = r
    return retval

def main():
    return 0


if __name__ == '__main__':
    exit(main())
