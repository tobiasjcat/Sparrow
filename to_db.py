#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

import csv
from pprint import pformat, pprint
import sqlite3
import sys
import time

db_conn = sqlite3.connect("calls.db")
c =  db_conn.cursor()

def main():
    tables = ["calls"]
    indexes = ["type_idx", "time_idx" , "location_idx"]
    # OperationError if '?' used
    for t in tables:
        c.execute("DROP TABLE IF EXISTS {}".format(t))
    for i in indexes:
        c.execute("DROP INDEX IF EXISTS {}".format(t))

    c.execute("""
CREATE TABLE calls (
    address TEXT,
    calltype TEXT,
    datetime TEXT,
    epoch_time INT,
    latitude TEXT,
    longitude TEXT,
    location TEXT,
    ic_num TEXT
    )""")

    db_conn.commit()

    #        11/23/2019 03:41:00 PM
    timefmt = "%m/%d/%Y %I:%M:%S %p"


    print("Loading csv into RAM...", end='')
    sys.stdout.flush()
    insert_lines = []
    with open("snnoc.csv") as csvfile:
        snnocreader = csv.DictReader(csvfile)
        for row in snnocreader:
            # print(row)
            temprow = [ \
                row["Address"], \
                row["Type"], \
                row["Datetime"], \
                int(time.mktime(time.strptime(row["Datetime"], timefmt))), \
                row["Latitude"], \
                row["Longitude"], \
                row["Report Location"], \
                row["Incident Number"], \
                ]
            if all(temprow):
                insert_lines.append(tuple(temprow))
    print("Done")
    print("Inserting rows into db...", end='')
    sys.stdout.flush()
    c.executemany("INSERT INTO calls VALUES (?,?,?,?,?,?,?,?)", insert_lines)
    print("Done")


    # pprint(c.execute("SELECT Count(address) FROM calls").fetchall())
#    pprint(c.execute("SELECT * FROM calls LIMIT 2").fetchall())

    print("Indexing...", end='')
    sys.stdout.flush()
    c.execute("CREATE INDEX type_idx ON calls(calltype)")
    c.execute("CREATE INDEX time_idx ON calls(epoch_time)")
    c.execute("CREATE INDEX location_idx ON calls(latitude, longitude)")
    # c.execute("CREATE INDEX type_idx ON calls(calltype)")
    print("Done")

    print("Committing...", end='')
    sys.stdout.flush()
    db_conn.commit()
    print("Done")

    return 0

if __name__ == '__main__':
    exit(main())
