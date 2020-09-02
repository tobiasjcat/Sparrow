#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

import sqlite3

conn = sqlite3.connect("stats.db")
c = conn.cursor()

def get_all_hours_data():
    return dict(c.execute("SELECT * FROM all_hour_of_the_day").fetchall())

def main():
    schema = c.execute("")
    return 0


if __name__ == '__main__':
    exit(main())
