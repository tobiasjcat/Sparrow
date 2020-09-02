#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

from collections import Counter
from pprint import pformat, pprint
import sqlite3
import sys
import time

call_conn = sqlite3.connect("calls.db")
cc = call_conn.cursor()
stat_conn = sqlite3.connect("stats.db")
sc = stat_conn.cursor()

DANGER = [ \
    "%Assault%", \
    "%Automatic Fire%", \
    "%Scenes Of Violence%", \
]

CHUNKSIZE = 6

def quick_print(instr):
    sys.stdout.write(instr)
    sys.stdout.flush()

def main():

    quick_print("Dropping and vacuuming...")
    tables = [ \
        "all_hour_of_the_day", \
        "danger_hour_of_the_day", \
        "all_day_of_the_week", \
        "danger_day_of_the_week", \
        ]
    for t in tables:
        sc.execute("DROP TABLE IF EXISTS {}".format(t))


    sc.execute("VACUUM")
    stat_conn.commit()
    print("Done")

    #all_hour_of_day
    quick_print("Inserting hour of the day data (all calls)...")
    sc.execute("CREATE TABLE all_hour_of_the_day (hour INT, num_calls INT)")
    hours = cc.execute("SELECT epoch_time FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    while chunk:
        insert_values = [time.localtime(i[0])[3] for i in chunk]
        results.update(insert_values)
        chunk = hours.fetchmany(CHUNKSIZE)
    to_insert = [(i, results[i], ) for i in range(24)]
    sc.executemany("INSERT INTO all_hour_of_the_day VALUES (?, ?)", to_insert)
    stat_conn.commit()
    print("Done")

    #danger_hour_of_the_day
    quick_print("Inserting hour of the day data (violent calls)...")
    sc.execute("CREATE TABLE danger_hour_of_the_day (hour INT, num_calls INT)")
    results = Counter([])
    for d in DANGER:
        hours = cc.execute("SELECT epoch_time FROM calls WHERE calltype LIKE '{}'".format(d))
        chunk = hours.fetchmany(CHUNKSIZE)
        while chunk:
            insert_values = [time.localtime(i[0])[3] for i in chunk]
            results.update(insert_values)
            chunk = hours.fetchmany(CHUNKSIZE)
    to_insert = [(i, results[i], ) for i in range(24)]
    sc.executemany("INSERT INTO danger_hour_of_the_day VALUES (?, ?)", to_insert)
    stat_conn.commit()
    print("Done")

    #all_day_of_the_week
    quick_print("Inserting day of the week data (all calls)...")
    sc.execute("CREATE TABLE all_day_of_the_week (hour INT, num_calls INT)")
    hours = cc.execute("SELECT epoch_time FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    while chunk:
        insert_values = [time.localtime(i[0])[6] for i in chunk]
        results.update(insert_values)
        chunk = hours.fetchmany(CHUNKSIZE)
    to_insert = [(i, results[i], ) for i in range(7)]
    sc.executemany("INSERT INTO all_day_of_the_week VALUES (?, ?)", to_insert)
    stat_conn.commit()
    print("Done")


    #danger_day_of_the_week
    quick_print("Inserting day of the week data (violent calls)...")
    sc.execute("CREATE TABLE danger_day_of_the_week (day INT, num_calls INT)")
    results = Counter([])
    for d in DANGER:
        hours = cc.execute("SELECT epoch_time FROM calls WHERE calltype LIKE '{}'".format(d))
        chunk = hours.fetchmany(CHUNKSIZE)
        while chunk:
            insert_values = [time.localtime(i[0])[6] for i in chunk]
            results.update(insert_values)
            chunk = hours.fetchmany(CHUNKSIZE)
    to_insert = [(i, results[i], ) for i in range(7)]
    sc.executemany("INSERT INTO danger_day_of_the_week VALUES (?, ?)", to_insert)
    stat_conn.commit()
    print("Done")




    return 0

if __name__ == '__main__':
    exit(main())
