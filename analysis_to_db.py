#!/usr/bin/env python3

#Paul Croft
#September 1, 2020

from collections import Counter
import itertools
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
        "all_hour_of_the_week", \
        "danger_hour_of_the_week", \
        "quadrants", \
        "non_larceny_quadrants", \
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
    sc.execute("CREATE TABLE all_day_of_the_week (day INT, num_calls INT)")
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


    #all_hour_of_the_week
    quick_print("Inserting hour of the week data (all calls)...")
    sc.execute("CREATE TABLE all_hour_of_the_week (day INT, hour INT, num_calls INT)")
    hours = cc.execute("SELECT epoch_time FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    while chunk:
        insert_values = ["{},{}".format(time.localtime(i[0])[6], time.localtime(i[0])[3]) for i in chunk]
        results.update(insert_values)
        chunk = hours.fetchmany(CHUNKSIZE)
    # to_insert = [(i, results[i], ) for i in range(7)]
    to_insert = []
    for d in range(7):
        for h in range(24):
            index_str = "{},{}".format(d,h)
            to_insert.append((d, h, results[index_str], ))
    sc.executemany("INSERT INTO all_hour_of_the_week VALUES (?, ?, ?)", to_insert)
    stat_conn.commit()
    print("Done")


    #danger_hour_of_the_week
    quick_print("Inserting hour of the week data (violent calls)...")
    sc.execute("CREATE TABLE danger_hour_of_the_week (day INT, hour INT, num_calls INT)")
    hours = cc.execute("SELECT epoch_time FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    for d in DANGER:
        hours = cc.execute("SELECT epoch_time FROM calls WHERE calltype LIKE '{}'".format(d))
        chunk = hours.fetchmany(CHUNKSIZE)
        while chunk:
            insert_values = ["{},{}".format(time.localtime(i[0])[6], time.localtime(i[0])[3]) for i in chunk]
            results.update(insert_values)
            chunk = hours.fetchmany(CHUNKSIZE)
    # to_insert = [(i, results[i], ) for i in range(7)]
    to_insert = []
    for d in range(7):
        for h in range(24):
            index_str = "{},{}".format(d,h)
            to_insert.append((d, h, results[index_str], ))
    sc.executemany("INSERT INTO danger_hour_of_the_week VALUES (?, ?, ?)", to_insert)
    stat_conn.commit()
    print("Done")

    #all_call_coordinates
    quick_print("Inserting coordinates (all calls)...")
    sc.execute("CREATE TABLE quadrants (latitude_hundredths INT, longitude_hundredths INT, num_calls INT)")
    hours = cc.execute("SELECT latitude, longitude FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    while chunk:
        # pprint(chunk)
        # insert_values = ["{},{}".format(time.localtime(i[0])[6], time.localtime(i[0])[3]) for i in chunk]
        insert_values = ["{},{}".format(int(float(x) * 100) - 4700, int(float(y) * 100) + 12300) for x,y in chunk]
        results.update(insert_values)
        chunk = hours.fetchmany(CHUNKSIZE)
    # pprint(results)
    to_insert = []
    #bounds of seattle
    for x in range(25, 78):
        for y in range(53, 112):
            to_insert.append((x,y,results["{},{}".format(x,y)]))

    sc.executemany("INSERT INTO quadrants VALUES (?, ?, ?)", to_insert)
    stat_conn.commit()
    print("Done")


    #non_larceny_call_coordinates
    quick_print("Inserting non_larceny_coordinates (all calls)...")
    sc.execute("CREATE TABLE non_larceny_quadrants (latitude_hundredths INT, longitude_hundredths INT, num_calls INT)")
    # hours = cc.execute("SELECT latitude, longitude FROM calls")
    chunk = hours.fetchmany(CHUNKSIZE)
    results = Counter([])
    for d in DANGER:
        hours = cc.execute("SELECT latitude, longitude FROM calls WHERE calltype LIKE '{}'".format(d))
        chunk = hours.fetchmany(CHUNKSIZE)
        while chunk:
            insert_values = ["{},{}".format(int(float(x) * 100) - 4700, int(float(y) * 100) + 12300) for x,y in chunk]
            results.update(insert_values)
            chunk = hours.fetchmany(CHUNKSIZE)
    # pprint(results)
    to_insert = []
    #bounds of seattle
    for x in range(25, 78):
        for y in range(53, 112):
            to_insert.append((x,y,results["{},{}".format(x,y)]))

    sc.executemany("INSERT INTO non_larceny_quadrants VALUES (?, ?, ?)", to_insert)
    stat_conn.commit()
    print("Done")




    return 0

if __name__ == '__main__':
    exit(main())
